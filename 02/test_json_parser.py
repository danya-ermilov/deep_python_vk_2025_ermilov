import unittest
from io import StringIO
from unittest.mock import (
    patch,
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

        expected_calls = [
            unittest.mock.call("key1", "WORD1"),
            unittest.mock.call("key1", "word2"),
        ]
        mock_callback.assert_has_calls(expected_calls, any_order=True)

    def test_print_called_with_correct_arguments(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key1", "KEY2"]
        tokens = ["WORD1", "word2"]

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            process_json(json_str, required_keys, tokens)

            output = mock_stdout.getvalue().strip().splitlines()

            expected_output = ["key='key1', token='WORD1'", "key='key1', token='word2'"]

            self.assertEqual(output, expected_output)

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

        def custom_callback(key, token):
            print(f"Found: {key}, {token}")

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            process_json(json_str, required_keys, tokens, custom_callback)

            output = mock_stdout.getvalue().strip().splitlines()

            expected_output = [
                'Found: key1, WORD1',
                'None',
                'Found: key1, word2',
                'None',
            ]

            self.assertEqual(output, expected_output)

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
