import unittest
from unittest.mock import (
    patch,
    MagicMock,
)

from predict_message import (
    predict_message_mood,
    SomeModel,
)


class TestPredictMessageMood(unittest.TestCase):
    def setUp(self):
        self.model_mock = MagicMock(spec=SomeModel)

        self.patcher = patch('predict_message.SomeModel', return_value=self.model_mock)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_called_value(self):
        self.model_mock.predict.return_value = 0.2

        predict_message_mood("test", 0.3, 0.8)

        self.model_mock.predict.assert_called_once_with("test")

    def test_boundary_values_less(self):
        self.model_mock.predict.return_value = 0.2999
        self.assertEqual(predict_message_mood("test", 0.3, 0.8), "неуд")

        self.model_mock.predict.return_value = 0.7999
        self.assertEqual(predict_message_mood("test", 0.3, 0.8), "норм")

    def test_boundary_values_more(self):
        self.model_mock.predict.return_value = 0.8001
        self.assertEqual(predict_message_mood("test", 0.3, 0.8), "отл")

        self.model_mock.predict.return_value = 0.3001
        self.assertEqual(predict_message_mood("test", 0.3, 0.8), "норм")

    def test_boundary_values(self):
        self.model_mock.predict.return_value = 0.8
        self.assertEqual(predict_message_mood("test", 0.3, 0.8), "отл")

        self.model_mock.predict.return_value = 0.3
        self.assertEqual(predict_message_mood("test", 0.3, 0.8), "норм")
