import unittest
from custom_list import CustomList


class TestCustomList(unittest.TestCase):
    def test_add(self):
        self.lst1 = CustomList([1, 2, 3])
        self.lst2 = CustomList([4, 5])
        self.lst3 = [7, 8, 9, 10]
        self.num = 10

        result = self.lst1 + self.lst2
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(result), [5, 7, 3])
        self.assertEqual(list(self.lst1), [1, 2, 3])
        self.assertEqual(list(self.lst2), [4, 5])
        self.assertIsInstance(result, CustomList)

        result = self.lst1 + self.lst3
        self.assertEqual(list(result), [8, 10, 12, 10])
        self.assertEqual(list(self.lst1), [1, 2, 3])
        self.assertEqual(list(self.lst3), [7, 8, 9, 10])
        self.assertIsInstance(result, CustomList)

        result = self.lst1 + self.num
        self.assertEqual(list(result), [11, 12, 13])
        self.assertEqual(list(self.lst1), [1, 2, 3])
        self.assertIsInstance(result, CustomList)

    def test_radd(self):
        self.lst1 = CustomList([1, 2, 3])
        self.lst3 = [7, 8, 9, 10]
        self.num = 10

        result = self.lst3 + self.lst1
        self.assertEqual(list(result), [8, 10, 12, 10])
        self.assertEqual(list(self.lst1), [1, 2, 3])
        self.assertEqual(list(self.lst3), [7, 8, 9, 10])
        self.assertIsInstance(result, CustomList)

        result = self.num + self.lst1
        self.assertEqual(list(result), [11, 12, 13])
        self.assertEqual(list(self.lst1), [1, 2, 3])
        self.assertIsInstance(result, CustomList)

    def test_sub(self):
        self.lst1 = CustomList([1, 2, 3])
        self.lst2 = CustomList([4, 5])
        self.lst3 = [7, 8, 9, 10]
        self.num = 10

        result = self.lst1 - self.lst2
        self.assertEqual(list(result), [-3, -3, 3])
        self.assertEqual(list(self.lst1), [1, 2, 3])
        self.assertEqual(list(self.lst2), [4, 5])
        self.assertIsInstance(result, CustomList)

        result = self.lst1 - self.lst3
        self.assertEqual(list(result), [-6, -6, -6, -10])
        self.assertEqual(list(self.lst1), [1, 2, 3])
        self.assertEqual(list(self.lst3), [7, 8, 9, 10])
        self.assertIsInstance(result, CustomList)

        result = self.lst1 - self.num
        self.assertEqual(list(result), [-9, -8, -7])
        self.assertEqual(list(self.lst1), [1, 2, 3])
        self.assertIsInstance(result, CustomList)

    def test_rsub(self):
        self.lst1 = CustomList([1, 2, 3])
        self.lst3 = [7, 8, 9, 10]
        self.num = 10

        result = self.lst3 - self.lst1
        self.assertEqual(list(result), [6, 6, 6, 10])
        self.assertEqual(list(self.lst1), [1, 2, 3])
        self.assertEqual(list(self.lst3), [7, 8, 9, 10])
        self.assertIsInstance(result, CustomList)

        result = self.num - self.lst1
        self.assertEqual(list(self.lst1), [1, 2, 3])
        self.assertEqual(list(result), [9, 8, 7])
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
        self.lst1 = CustomList([1, 2, 3])
        self.lst2 = CustomList([4, 5])
        self.lst3 = [7, 8, 9, 10]

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
        self.lst1 = CustomList([1, 2, 3])
        self.assertEqual(str(self.lst1), "Элементы: 1, 2, 3\nСумма: 6")
