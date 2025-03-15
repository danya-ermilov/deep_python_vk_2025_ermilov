import unittest

from predict_message import predict_message_mood

class TestFileinGenerator(unittest.TestCase):
    def test_bad_w_args(self):
        string = "....less half...."
        result = predict_message_mood(string, 0.6, 1)
        self.assertEqual(result, "неуд")

    def test_bad_wo_args(self):
        string = ".....l_h......"
        result = predict_message_mood(string)
        self.assertEqual(result, "неуд")

    def test_ok_w_args(self):
        string = "half...."
        result = predict_message_mood(string, 0.1, 0.9)
        self.assertEqual(result, "норм")

    def test_ok_wo_args(self):
        string = "half...."
        result = predict_message_mood(string)
        self.assertEqual(result, "норм")

    def test_ok_w_args(self):
        string = "more half...."
        result = predict_message_mood(string, 0.1, 0.5)
        self.assertEqual(result, "отл")

    def test_ok_wo_args(self):
        string = "more half"
        result = predict_message_mood(string)
        self.assertEqual(result, "отл")