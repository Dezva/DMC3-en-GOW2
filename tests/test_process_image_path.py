"""Windows-only checks for the limited-rights process image query.

Load only the helper from the client AST: no game, PINE or report is opened.
"""
import base64
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
PWSH = os.environ.get("PWSH_BIN") or shutil.which("pwsh") or shutil.which("powershell")


@unittest.skipUnless(sys.platform == "win32" and PWSH, "Windows and PowerShell required")
class ProcessImagePathTests(unittest.TestCase):
    def query(self, body):
        source = str(ROOT / "tools" / "Probe-Pine.ps1").replace("'", "''")
        command = """
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$tokens = $null; $parseErrors = $null
$ast = [Management.Automation.Language.Parser]::ParseFile('%s', [ref]$tokens, [ref]$parseErrors)
if ($parseErrors.Count) { throw 'Client has PowerShell parse errors.' }
$definition = $ast.Find({ param($node)
    $node -is [Management.Automation.Language.FunctionDefinitionAst] -and
    $node.Name -eq 'Get-LimitedProcessImagePath'
}, $true)
if ($null -eq $definition) { throw 'Image query helper missing.' }
Invoke-Expression $definition.Extent.Text
%s
""" % (source, body)
        encoded = base64.b64encode(command.encode("utf-16-le")).decode("ascii")
        result = subprocess.run(
            [PWSH, "-NoProfile", "-NonInteractive", "-EncodedCommand", encoded],
            capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_current_process_image_matches_powershell_executable(self):
        result = self.query("""
$expected = [Diagnostics.Process]::GetCurrentProcess().MainModule.FileName
$actual = Get-LimitedProcessImagePath $PID
@{ expected = $expected; actual = $actual } | ConvertTo-Json -Compress
""")
        self.assertEqual(os.path.normcase(result["actual"]), os.path.normcase(result["expected"]))
        self.assertTrue(Path(result["actual"]).is_absolute())

    def test_invalid_pid_is_error_not_a_confirmed_path(self):
        result = self.query("""
$failed = $false; $path = $null
try { $path = Get-LimitedProcessImagePath 0 } catch { $failed = $true }
@{ failed = $failed; path = $path } | ConvertTo-Json -Compress
""")
        self.assertTrue(result["failed"])
        self.assertIsNone(result["path"])


if __name__ == "__main__":
    unittest.main()
