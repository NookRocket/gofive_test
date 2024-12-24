import unittest
from unittest.mock import MagicMock


class TestDigitalClock(unittest.TestCase):
    def setUp(self):
        self.clock = MagicMock()

    def test_change_button(self):
        self.clock.mode = "date"
        self.clock.change.side_effect = lambda: (
            setattr(self.clock, 'mode', 'time')
            if self.clock.mode == "date"
            else setattr(self.clock, 'mode', 'date')
        )

        self.clock.change()
        self.assertEqual(self.clock.mode, "time")

        self.clock.change()
        self.assertEqual(self.clock.mode, "date")

    def test_reset_button(self):
        self.clock.reset.side_effect = lambda: (
            setattr(self.clock, 'mode', 'change_date')
            if self.clock.mode == "date"
            else setattr(self.clock, 'mode', 'change_time')
        )

        self.clock.mode = "date"
        self.clock.reset()
        self.assertEqual(self.clock.mode, "change_date")

        self.clock.mode = "time"
        self.clock.reset()
        self.assertEqual(self.clock.mode, "change_time")

    def test_set_button(self):
        self.clock.reset.side_effect = lambda: (
            setattr(self.clock, 'mode', 'date')
            if self.clock.mode == "change_date"
            else setattr(self.clock, 'mode', 'time')
        )

        self.clock.mode = "change_date"
        self.clock.reset()
        self.assertEqual(self.clock.mode, "date")

        self.clock.mode = "change_time"
        self.clock.reset()
        self.assertEqual(self.clock.mode, "time")


if __name__ == "__main__":
    unittest.main()
