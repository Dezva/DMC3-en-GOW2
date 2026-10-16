"""Small Windows x64 read-only backend. No privilege adjustment or write API."""
import ctypes
from ctypes import wintypes as w
from dataclasses import dataclass
import os
import struct


QUERY_LIMITED = 0x1000
QUERY_READ = 0x0400 | 0x0010  # VirtualQueryEx requires QUERY_INFORMATION.
MAX_READ = 4096
MAX_USER = 0x00007FFFFFFFFFFF
READABLE = {0x02, 0x04, 0x08, 0x20, 0x40, 0x80}


class ModuleInfo(ctypes.Structure):
    _fields_ = [("base", ctypes.c_void_p), ("size", w.DWORD), ("entry", ctypes.c_void_p)]


class MemoryBasicInformation(ctypes.Structure):
    _fields_ = [("base", ctypes.c_void_p), ("allocation", ctypes.c_void_p),
                ("allocation_protect", w.DWORD), ("partition", w.WORD),
                ("size", ctypes.c_size_t), ("state", w.DWORD),
                ("protect", w.DWORD), ("kind", w.DWORD)]


class ObservationError(Exception):
    def __init__(self, stage, message, *, winerror=None, **details):
        super().__init__(message)
        self.data = dict(stage=stage, message=message, winerror=winerror, **details)


def valid_pointer(address, size=1, alignment=1):
    return (isinstance(address, int) and size > 0 and address >= 0x10000
            and address % alignment == 0 and address + size - 1 <= MAX_USER)


@dataclass
class Page:
    base: int
    size: int
    state: int
    protect: int
    kind: int = 0
    allocation: int = 0


def read_exact(memory, address, size):
    if size > MAX_READ or not valid_pointer(address, size):
        raise ObservationError("pointer", "Invalid address or read size", address=address, requested=size)
    cursor = address
    while cursor < address + size:
        page = memory.query(cursor)
        if (page.base > cursor or page.base + page.size <= cursor or page.state != 0x1000
                or page.protect & (0x100 | 0x01) or page.protect & 0xFF not in READABLE):
            raise ObservationError("page", "Uncommitted, guarded or unreadable page", address=cursor)
        cursor = min(address + size, page.base + page.size)
    data = memory.read(address, size)
    if len(data) != size:
        raise ObservationError("read", "Partial read rejected", address=address,
                               requested=size, transferred=len(data))
    return data


def unpack(memory, address, fmt):
    return struct.unpack(fmt, read_exact(memory, address, struct.calcsize(fmt)))


class WindowsMemory:
    def __init__(self):
        if os.name != "nt" or ctypes.sizeof(ctypes.c_void_p) != 8:
            raise ObservationError("platform", "A native Windows x64 observer is required")
        self.k = ctypes.WinDLL("kernel32", use_last_error=True)
        self.psapi = ctypes.WinDLL("psapi", use_last_error=True)
        self.handle = None
        self.read_calls = 0
        self.read_bytes = 0
        self.pid = None
        self._bind()

    def _bind(self):
        def bind(lib, name, args, result):
            fn = getattr(lib, name)
            fn.argtypes, fn.restype = args, result
            return fn
        ptr = ctypes.c_void_p
        self.open = bind(self.k, "OpenProcess", [w.DWORD, w.BOOL, w.DWORD], w.HANDLE)
        self.close_handle = bind(self.k, "CloseHandle", [w.HANDLE], w.BOOL)
        self.image_name = bind(self.k, "QueryFullProcessImageNameW",
                               [w.HANDLE, w.DWORD, w.LPWSTR, ctypes.POINTER(w.DWORD)], w.BOOL)
        self.times = bind(self.k, "GetProcessTimes", [w.HANDLE] + [ctypes.POINTER(w.FILETIME)] * 4, w.BOOL)
        self.exit_code = bind(self.k, "GetExitCodeProcess", [w.HANDLE, ctypes.POINTER(w.DWORD)], w.BOOL)
        self.rpm = bind(self.k, "ReadProcessMemory",
                        [w.HANDLE, ptr, ptr, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)], w.BOOL)
        self.vq = bind(self.k, "VirtualQueryEx", [w.HANDLE, ptr, ptr, ctypes.c_size_t], ctypes.c_size_t)
        self.enum_pids = bind(self.psapi, "EnumProcesses",
                              [ctypes.POINTER(w.DWORD), w.DWORD, ctypes.POINTER(w.DWORD)], w.BOOL)
        self.enum_modules = bind(self.psapi, "EnumProcessModulesEx",
                                 [w.HANDLE, ctypes.POINTER(ptr), w.DWORD, ctypes.POINTER(w.DWORD), w.DWORD], w.BOOL)
        self.module_info = bind(self.psapi, "GetModuleInformation", [w.HANDLE, ptr, ptr, w.DWORD], w.BOOL)
        user = ctypes.WinDLL("user32", use_last_error=True)
        self.foreground_window = bind(user, "GetForegroundWindow", [], w.HWND)
        self.window_pid = bind(user, "GetWindowThreadProcessId", [w.HWND, ctypes.POINTER(w.DWORD)], w.DWORD)

    @staticmethod
    def fail(stage, **details):
        error = ctypes.get_last_error()
        raise ObservationError(stage, ctypes.FormatError(error).strip(), winerror=error, **details)

    def path(self, handle):
        buf = ctypes.create_unicode_buffer(32768)
        size = w.DWORD(len(buf))
        if not self.image_name(handle, 0, buf, ctypes.byref(size)):
            self.fail("image_path")
        return buf.value

    def creation(self, handle):
        values = [w.FILETIME() for _ in range(4)]
        if not self.times(handle, *(ctypes.byref(v) for v in values)):
            self.fail("process_time")
        return values[0].dwHighDateTime << 32 | values[0].dwLowDateTime

    def token_context(self, handle):
        """Read only integrity/elevation metadata; never modify either token."""
        adv = ctypes.WinDLL("advapi32", use_last_error=True)
        adv.OpenProcessToken.argtypes = [w.HANDLE, w.DWORD, ctypes.POINTER(w.HANDLE)]
        adv.OpenProcessToken.restype = w.BOOL
        adv.GetTokenInformation.argtypes = [w.HANDLE, ctypes.c_int, ctypes.c_void_p,
                                            w.DWORD, ctypes.POINTER(w.DWORD)]
        adv.GetTokenInformation.restype = w.BOOL
        adv.GetSidSubAuthorityCount.argtypes = [ctypes.c_void_p]
        adv.GetSidSubAuthorityCount.restype = ctypes.POINTER(ctypes.c_ubyte)
        adv.GetSidSubAuthority.argtypes = [ctypes.c_void_p, w.DWORD]
        adv.GetSidSubAuthority.restype = ctypes.POINTER(w.DWORD)
        token = w.HANDLE()
        if not adv.OpenProcessToken(handle, 0x0008, ctypes.byref(token)):  # TOKEN_QUERY
            self.fail("token_query")
        try:
            elevation = w.DWORD()
            size = w.DWORD()
            if not adv.GetTokenInformation(token, 20, ctypes.byref(elevation), 4, ctypes.byref(size)):
                self.fail("token_elevation")
            adv.GetTokenInformation(token, 25, None, 0, ctypes.byref(size))
            if not 16 <= size.value <= 4096:
                raise ObservationError("token_integrity", "Unexpected token metadata size")
            buf = ctypes.create_string_buffer(size.value)
            if not adv.GetTokenInformation(token, 25, buf, len(buf), ctypes.byref(size)):
                self.fail("token_integrity")
            sid = ctypes.cast(buf, ctypes.POINTER(ctypes.c_void_p))[0]
            count = adv.GetSidSubAuthorityCount(sid)[0]
            rid = adv.GetSidSubAuthority(sid, count - 1)[0]
            return dict(elevated=bool(elevation.value), integrity_rid=rid)
        finally:
            self.close_handle(token)

    def discover(self, expected_path):
        pids = (w.DWORD * 8192)()
        used = w.DWORD()
        if not self.enum_pids(pids, ctypes.sizeof(pids), ctypes.byref(used)):
            self.fail("enumerate_processes")
        if used.value == ctypes.sizeof(pids):
            raise ObservationError("enumerate_processes", "PID buffer full; enumeration incomplete")
        found = []
        for pid in pids[:used.value // 4]:
            handle = self.open(QUERY_LIMITED, False, pid)
            if not handle:
                continue  # Unrelated inaccessible processes are not inspected.
            try:
                path = self.path(handle)
                if os.path.normcase(os.path.realpath(path)) == os.path.normcase(os.path.realpath(expected_path)):
                    found.append(dict(pid=pid, path=path, creation_filetime=self.creation(handle)))
            except ObservationError:
                continue
            finally:
                self.close_handle(handle)
        if len(found) != 1:
            raise ObservationError("discovery", "Expected exactly one readable identity at the configured path",
                                   matching_processes=found, inaccessible_processes="not classified")
        return found[0]

    def attach(self, identity):
        self.pid = identity["pid"]
        self.handle = self.open(QUERY_READ, False, self.pid)
        if not self.handle:
            self.fail("open_query_read", pid=self.pid, requested_access=QUERY_READ)
        if self.path(self.handle) != identity["path"] or self.creation(self.handle) != identity["creation_filetime"]:
            raise ObservationError("process_changed", "PID/path/start changed during attachment")
        self.identity = identity

    def alive(self):
        value = w.DWORD()
        if not self.exit_code(self.handle, ctypes.byref(value)):
            self.fail("process_status")
        return value.value == 259 and self.creation(self.handle) == self.identity["creation_filetime"]

    def foreground(self):
        # Passive ownership check only: no focus changes, keys or window control.
        window = self.foreground_window()
        if not window:
            return False
        pid = w.DWORD()
        if not self.window_pid(window, ctypes.byref(pid)):
            self.fail("foreground_query")
        return pid.value == self.pid

    def image(self):
        modules = (ctypes.c_void_p * 1)()
        used = w.DWORD()
        if not self.enum_modules(self.handle, modules, ctypes.sizeof(modules), ctypes.byref(used), 2):
            self.fail("image_base")
        if used.value < 8 or not modules[0]:
            raise ObservationError("image_base", "No main module returned")
        info = ModuleInfo()
        if not self.module_info(self.handle, modules[0], ctypes.byref(info), ctypes.sizeof(info)):
            self.fail("image_information")
        return dict(base=info.base, size=info.size, entry=info.entry)

    def query(self, address):
        info = MemoryBasicInformation()
        count = self.vq(self.handle, address, ctypes.byref(info), ctypes.sizeof(info))
        if count != ctypes.sizeof(info):
            self.fail("virtual_query", address=address, returned=count)
        return Page(info.base or 0, info.size, info.state, info.protect, info.kind, info.allocation or 0)

    def read(self, address, size):
        buf = ctypes.create_string_buffer(size)
        count = ctypes.c_size_t()
        self.read_calls += 1
        ctypes.set_last_error(0)
        success = self.rpm(self.handle, address, buf, size, ctypes.byref(count))
        self.read_bytes += count.value
        if not success:
            self.fail("read_process_memory", address=address, requested=size,
                      transferred=count.value, success=bool(success))
        if count.value != size:
            raise ObservationError("read_process_memory", "Partial read rejected", address=address,
                                   requested=size, transferred=count.value, success=True)
        return buf.raw

    def close(self):
        if self.handle:
            self.close_handle(self.handle)
            self.handle = None
