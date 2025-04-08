import unittest
from descriptor import Example


class TestDescriptors(unittest.TestCase):
    def setUp(self):
        self.obj = Example(10, 20.5, "test")

    def test_initial_values(self):
        self.assertEqual(self.obj.integer, 10)
        self.assertEqual(self.obj.double, 20.5)
        self.assertEqual(self.obj.string, "test")
        self.assertEqual(self.obj.__dict__, {"_integer": 10, "_double": 20.5, "_string": "test"})

    def test_change_values_correct_types(self):
        self.obj.integer = 20
        self.obj.double = 30.5
        self.obj.string = "new value"

        self.assertEqual(self.obj.integer, 20)
        self.assertEqual(self.obj.double, 30.5)
        self.assertEqual(self.obj.string, "new value")

    def test_wrong_types(self):
        with self.assertRaises(ValueError):
            self.obj.integer = "not an integer"

        with self.assertRaises(ValueError):
            self.obj.double = "not a double"

        with self.assertRaises(ValueError):
            self.obj.string = 123

    def test_instance_dict_consistency(self):
        self.obj.integer = 30
        self.assertEqual(self.obj.__dict__["_integer"], 30)

    def test_descriptor_independence(self):
        obj2 = Example(5, 10.5, "second")

        self.obj.integer = 100
        self.assertEqual(self.obj.integer, 100)
        self.assertEqual(obj2.integer, 5)
