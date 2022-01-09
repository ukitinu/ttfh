import unittest

from src.saves import SaveState


class SavesTest(unittest.TestCase):

    def test_eq(self):
        s1 = SaveState("name", 1, 1, 1)
        s2 = SaveState("name", 2, 2, 2)
        s3 = SaveState("other", 1, 1, 1)
        self.assertEqual(s1, s2)
        self.assertNotEqual(s1, s3)

        class TestName:
            def __init__(self, name):
                self.name = name

        self.assertNotEqual(s1, TestName("name"))

    def test_str(self):
        self.assertEqual('"name", day 1 at 01:55', str(SaveState("name", 1, 1, 55)))
        self.assertEqual('"my name", day 2 at 00:10', str(SaveState("my name", 2, 0, 10)))
        self.assertEqual('"NAME", day 3 at 11:00', str(SaveState("NAME", 3, 11, 0)))

    def test_repr(self):
        self.assertEqual("name@1.01.55", repr(SaveState("name", 1, 1, 55)))
        self.assertEqual("my name@2.00.10", repr(SaveState("my name", 2, 0, 10)))
        self.assertEqual("NAME@3.11.00", repr(SaveState("NAME", 3, 11, 0)))

    def test_get_time_str(self):
        self.assertEqual("Day 1, hour 1, min 55", SaveState("name", 1, 1, 55).get_time_str())
        self.assertEqual("Day 2, hour 0, min 10", SaveState("my name", 2, 0, 10).get_time_str())
        self.assertEqual("Day 3, hour 11, min 0", SaveState("NAME", 3, 11, 0).get_time_str())

    def test_is_name_valid(self):
        self.assertTrue(SaveState.is_name_valid('A Valid Name'))
        self.assertTrue(SaveState.is_name_valid('name 1234'))

        self.assertFalse(SaveState.is_name_valid('x' * SaveState.NAME_LEN + 'x'))
        self.assertFalse(SaveState.is_name_valid('invalid-symbol'))

    def test_is_time_valid(self):
        self.assertTrue(SaveState.is_time_valid(1, 10, 25))
        self.assertTrue(SaveState.is_time_valid(3, 0, 59))

        self.assertFalse(SaveState.is_time_valid(1, 24, 30))
        self.assertFalse(SaveState.is_time_valid(2, 0, 60))
        self.assertFalse(SaveState.is_time_valid(0, 5, 30))

    def test_from_str(self):
        self.assertEqual(
            repr(SaveState('name123', 2, 8, 30)),
            repr(SaveState.from_str('name123@2.08.30'))
        )
        self.assertEqual(
            repr(SaveState('my save title', 1, 0, 0)),
            repr(SaveState.from_str('my save title@1.00.00'))
        )
        self.assertEqual(
            repr(SaveState('SaVeNaMe', 3, 23, 9)),
            repr(SaveState.from_str('SaVeNaMe@3.23.09'))
        )

    def test_from_str_error(self):
        with self.assertRaises(ValueError):
            SaveState.from_str('nameonly')  # no time
        with self.assertRaises(ValueError):
            SaveState.from_str('1.10.30')  # no name
        with self.assertRaises(ValueError):
            SaveState.from_str('symbols?@2.10.45')  # invalid name
        with self.assertRaises(ValueError):
            SaveState.from_str('two@names@1.03.15')  # two @
        with self.assertRaises(ValueError):
            SaveState.from_str('My name@2.24.41')  # hour is 24
        with self.assertRaises(ValueError):
            SaveState.from_str('My name@3.19.60')  # min is 60

    def test_from_str_all_values(self):
        for d in range(1, 4):
            for h in range(0, 24):
                for m in range(0, 60):
                    self.assertEqual(
                        repr(SaveState('name', d, h, m)),
                        repr(SaveState.from_str(f'name@{d}.{h:02}.{m:02}'))
                    )


if __name__ == '__main__':
    unittest.main()
