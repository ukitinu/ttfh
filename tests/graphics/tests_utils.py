import unittest

from src.graphics.utils import calc_arc_extent


class UtilsTest(unittest.TestCase):

    def test_calc_arc_extent_hour_start(self):
        self.assertEqual(0, calc_arc_extent(1, 5, 0))

        for d in range(1, 4):
            for h in range(0, 24):
                if d != 1 or h != 5:
                    self.assertEqual(-359, calc_arc_extent(d, h, 0))

    def test_calc_arc_extent_quarters(self):
        self.assertEqual(-90, calc_arc_extent(2, 12, 15))
        self.assertEqual(-180, calc_arc_extent(1, 19, 30))
        self.assertEqual(-270, calc_arc_extent(3, 12, 45))

    def test_calc_arc_extent_invariance(self):
        for m in range(0, 60):
            expected = calc_arc_extent(1, 6, m)
            for d in range(1, 4):
                for h in range(0, 24):
                    if d != 1 or h != 5:
                        self.assertEqual(expected, calc_arc_extent(d, h, m))


if __name__ == '__main__':
    unittest.main()
