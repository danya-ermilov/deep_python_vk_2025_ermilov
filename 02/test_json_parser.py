import unittest
from unittest.mock import (
    Mock,
)

from json_parser import process_json


class TestProcessJson(unittest.TestCase):
    def test_callback_called_with_correct_arguments(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key1", "KEY2"]
        tokens = ["WORD1", "word2"]

        mock_callback = Mock()
        process_json(json_str, required_keys, tokens, mock_callback)

        calls = mock_callback.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0].args, ("key1", "WORD1"))
        self.assertEqual(calls[1].args, ("key1", "word2"))

    def test_no_callback_calls_when_no_matches(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key3"]
        tokens = ["WORD1"]

        mock_callback = Mock()

        process_json(json_str, required_keys, tokens, mock_callback)

        mock_callback.assert_not_called()

    def test_callback_called_with_custom_logic(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key1", "KEY2"]
        tokens = ["WORD1", "word2"]

        mock_callback = Mock(return_value="custom_callback")
        process_json(json_str, required_keys, tokens, mock_callback)

        calls = mock_callback.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0].args, ("key1", "WORD1"))
        self.assertEqual(calls[1].args, ("key1", "word2"))

    def test_invalid_json(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"'

        with self.assertRaises(ValueError) as context:
            process_json(json_str)

        self.assertEqual(str(context.exception), "Invalid JSON string")

    def test_token_not_in_value(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key1", "KEY2"]
        tokens = ["WORD3"]

        mock_callback = Mock()

        process_json(json_str, required_keys, tokens, mock_callback)

        mock_callback.assert_not_called()

    def test_multiple_required_keys_with_matches(self):
        json_str = '{"key1": "word1 word2", "key2": "word1 word3", "key3": "word4"}'
        required_keys = ["key1", "key2"]
        tokens = ["word1"]

        mock_callback = Mock()
        process_json(json_str, required_keys, tokens, mock_callback)

        calls = mock_callback.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0].args, ("key1", "word1"))
        self.assertEqual(calls[1].args, ("key2", "word1"))

    def test_multiple_tokens_in_same_value(self):
        json_str = '{"key1": "word1 word2 word3", "key2": "word4"}'
        required_keys = ["key1"]
        tokens = ["word1", "word2", "word3"]

        mock_callback = Mock()
        process_json(json_str, required_keys, tokens, mock_callback)

        calls = mock_callback.call_args_list
        self.assertEqual(len(calls), 3)
        self.assertEqual(calls[0].args, ("key1", "word1"))
        self.assertEqual(calls[1].args, ("key1", "word2"))
        self.assertEqual(calls[2].args, ("key1", "word3"))

    def test_multiple_matches_across_keys_and_tokens(self):
        json_str = '{"key1": "word1 word2", "key2": "word2 word3", "key3": "word1 word3"}'
        required_keys = ["key1", "key2", "key3"]
        tokens = ["word1", "word2", "word3"]

        mock_callback = Mock()
        process_json(json_str, required_keys, tokens, mock_callback)

        calls = mock_callback.call_args_list
        self.assertEqual(len(calls), 6)
        expected_calls = [
            ("key1", "word1"), ("key1", "word2"),
            ("key2", "word2"), ("key2", "word3"),
            ("key3", "word1"), ("key3", "word3")
        ]
        actual_calls = [call.args for call in calls]
        for expected in expected_calls:
            self.assertIn(expected, actual_calls)
