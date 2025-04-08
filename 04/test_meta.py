import unittest
from meta import CustomClass


class TestCustomMeta(unittest.TestCase):
    def setUp(self):
        self.inst = CustomClass()

    def test_class_attributes(self):
        self.assertEqual(CustomClass.custom_x, 50)
        with self.assertRaises(AttributeError):
            _ = CustomClass.x

    def test_instance_attributes(self):
        self.assertEqual(self.inst.custom_x, 50)
        self.assertEqual(self.inst.custom_val, 99)
        self.assertEqual(self.inst.custom_line(), 100)
        self.assertEqual(str(self.inst), "Custom_by_metaclass")

    def test_original_attributes_blocked(self):
        with self.assertRaises(AttributeError):
            _ = self.inst.x
        with self.assertRaises(AttributeError):
            _ = self.inst.val
        with self.assertRaises(AttributeError):
            self.inst.line()
        with self.assertRaises(AttributeError):
            _ = self.inst.yyy

    def test_dynamic_attributes(self):
        self.inst.dynamic = "added later"
        self.assertEqual(self.inst.custom_dynamic, "added later")
        with self.assertRaises(AttributeError):
            _ = self.inst.dynamic
