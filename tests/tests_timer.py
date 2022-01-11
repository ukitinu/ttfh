import unittest

from src.timer import Clock


class TimerTest(unittest.TestCase):
    def setUp(self) -> None:
        super(TimerTest, self).setUp()
        self.clock = Clock()

    def test_un_pause(self):
        self.assertFalse(self.clock.running)

        self.clock.un_pause('stop')
        self.assertFalse(self.clock.running)

        self.clock.un_pause('run')
        self.assertTrue(self.clock.running)
        self.clock.un_pause('run')
        self.assertTrue(self.clock.running)

        self.clock.un_pause('switch')
        self.assertFalse(self.clock.running)
        self.clock.un_pause('switch')
        self.assertTrue(self.clock.running)
        self.clock.un_pause()
        self.assertFalse(self.clock.running)

    def test_get_time_str(self):
        self.assertEqual('1.05.00', self.clock.get_time_str())
        self.clock.set_time(3, 8, 9)
        self.assertEqual('3.08.09', self.clock.get_time_str())
        self.clock.set_time(2, 11, 45)
        self.assertEqual('2.11.45', self.clock.get_time_str())


if __name__ == '__main__':
    unittest.main()
