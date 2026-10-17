"""Synthetic cue/CLI tests: no Windows audio, memory or game processes."""
import contextlib
import io
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import observe_dmc3 as observer


class CueTests(unittest.TestCase):
    def test_no_cue_before_target_or_when_disabled(self):
        def forbidden(*args):
            self.fail("No tone/event permitted here")
        self.assertFalse(observer.maybe_action_cue(forbidden, None, 10, beep=forbidden))
        self.assertFalse(observer.maybe_action_cue(forbidden, 5, 4.99, beep=forbidden))

    def test_one_bounded_tone_bracketed_and_no_action_inferred(self):
        order = []
        emitted = observer.maybe_action_cue(lambda stage, data: order.append((stage, data)), 5, 5.02,
                                             beep=lambda hz, ms: order.append((hz, ms)))
        self.assertTrue(emitted)
        self.assertEqual([order[0][0], order[1], order[2][0]],
                         ["sampling.action_cue.begin", (1200, 60), "sampling.action_cue.end"])
        self.assertTrue(order[0][1]["cue_only"])
        self.assertTrue(order[0][1]["actual_action_unknown"])
        self.assertEqual(order[0][1]["actual_elapsed_seconds"], 5.02)
        observer.maybe_action_cue(lambda *a: self.fail("Repeated event"), 5, 6, emitted,
                                 beep=lambda *a: self.fail("Repeated tone"))

    def test_delayed_cue_preserves_delay_not_false_planned_time(self):
        events = []
        observer.maybe_action_cue(lambda stage, data: events.append(data), 5, 5.4, beep=lambda *a: None)
        self.assertEqual(events[0]["planned_seconds"], 5)
        self.assertEqual(events[0]["actual_elapsed_seconds"], 5.4)

    def test_sound_failure_is_logged_and_propagated(self):
        events = []
        def failure(*args):
            raise OSError("synthetic audio failure")
        with self.assertRaises(OSError):
            observer.maybe_action_cue(lambda stage, data: events.append((stage, data)), 5, 5, beep=failure)
        self.assertFalse(events[-1][1]["sound_call_succeeded"])

    def test_invalid_cli_cues_never_start_capture(self):
        options = [["--action-cue-seconds", "5"],
                   ["--beep", "--action-cue-seconds", "0"],
                   ["--beep", "--action-cue-seconds", "nan"],
                   ["--beep", "--action-cue-seconds", "inf"],
                   ["--beep", "--action-cue-seconds", "9.5"],
                   ["--beep", "--action-cue-seconds", "5", "--access-only"],
                   ["--beep", "--action-cue-seconds", "5", "--annotate", "synthetic"]]
        for args in options:
            with self.subTest(args=args), patch.object(observer, "capture") as capture, \
                    contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                observer.main(args)
            capture.assert_not_called()

    def test_valid_cli_passes_single_cue_to_capture_without_game_access(self):
        with patch.object(observer, "capture", return_value=0) as capture:
            self.assertEqual(observer.main(["--samples", "200", "--hz", "10", "--beep",
                                           "--lead-in-seconds", "25", "--action-cue-seconds", "5"]), 0)
        self.assertEqual(capture.call_args.args[0].action_cue_seconds, 5)

    def test_default_keeps_cues_disabled(self):
        with patch.object(observer, "capture", return_value=0) as capture:
            observer.main([])
        self.assertIsNone(capture.call_args.args[0].action_cue_seconds)


if __name__ == "__main__":
    unittest.main()
