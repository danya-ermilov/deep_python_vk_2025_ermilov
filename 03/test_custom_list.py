import unittest
from custom_list import CustomList


class TestCustomList(unittest.TestCase):
    def setUp(self):
        self.lst1 = CustomList([1, 2, 3])
        self.lst2 = CustomList([4, 5])
        self.lst3 = [7, 8, 9]
        self.num = 10

    def test_add(self):
        result = self.lst1 + self.lst2
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(result), [5, 7, 3])
        self.assertEqual(str(result), "Элементы: 5, 7, 3\nСумма: 15")
        self.assertIsInstance(result, CustomList)

        result = self.lst1 + self.lst3
        self.assertEqual(list(result), [8, 10, 12])
        self.assertIsInstance(result, CustomList)

        result = self.lst1 + self.num
        self.assertEqual(list(result), [11, 2, 3])
        self.assertIsInstance(result, CustomList)

    def test_radd(self):
        result = self.lst3 + self.lst1
        self.assertEqual(list(result), [8, 10, 12])
        self.assertIsInstance(result, CustomList)

        result = self.num + self.lst1
        self.assertEqual(list(result), [11, 2, 3])
        self.assertIsInstance(result, CustomList)

    def test_sub(self):
        result = self.lst1 - self.lst2
        self.assertEqual(list(result), [-3, -3, 3])
        self.assertIsInstance(result, CustomList)

        result = self.lst1 - self.lst3
        self.assertEqual(list(result), [-6, -6, -6])
        self.assertIsInstance(result, CustomList)

        result = self.lst1 - self.num
        self.assertEqual(list(result), [-9, 2, 3])
        self.assertIsInstance(result, CustomList)

    def test_rsub(self):
        result = self.lst3 - self.lst1
        self.assertEqual(list(result), [6, 6, 6])
        self.assertIsInstance(result, CustomList)

        result = self.num - self.lst1
        self.assertEqual(list(result), [9, -2, -3])
        self.assertIsInstance(result, CustomList)

    def test_comparison(self):
        self.assertTrue(CustomList([6]) == CustomList([1, 2, 3]))
        self.assertFalse(CustomList([1, 2]) == CustomList([1, 3]))

        self.assertTrue(CustomList([1, 2, 3]) > CustomList([1, 2]))
        self.assertFalse(CustomList([1]) > CustomList([1, 2]))

        self.assertTrue(CustomList([1]) < [1, 2])
        self.assertFalse(CustomList([1, 2]) < [1])

        self.assertTrue(CustomList([6]) >= CustomList([1, 2]))
        self.assertFalse(CustomList([1]) >= CustomList([1, 2]))

        self.assertTrue(CustomList([6]) <= CustomList([1, 2, 3, 4]))
        self.assertFalse(CustomList([1, 2, 3]) <= CustomList([1, 3]))

        self.assertTrue(CustomList([1, 2]) != CustomList([1, 3]))
        self.assertFalse(CustomList([6]) != CustomList([1, 2, 3]))

    def test_type_error(self):
        with self.assertRaises(TypeError):
            self.lst1 == "invalid"

        with self.assertRaises(TypeError):
            self.lst1 < 123.45

        with self.assertRaises(TypeError):
            self.lst1 > 123.45

        with self.assertRaises(TypeError):
            self.lst1 != 123.45

        with self.assertRaises(TypeError):
            self.lst1 <= 123.45

        with self.assertRaises(TypeError):
            self.lst1 >= 123.45

    def test_str(self):
        self.assertEqual(str(self.lst1), "Элементы: 1, 2, 3\nСумма: 6")
