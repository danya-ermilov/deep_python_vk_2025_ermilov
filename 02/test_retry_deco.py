import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from retry_deco import retry_deco


class TestRetryDeco(unittest.TestCase):
    def setUp(self):
        self.mock_func = MagicMock()
        self.mock_func.__name__ = "test_func"

    def test_preserves_function_metadata(self):
        @retry_deco(max_tries=3)
        def sample_func(x):
            return x * 2

        self.assertEqual(sample_func.__name__, "sample_func")

    def test_success_on_first_attempt(self):
        self.mock_func.return_value = "success"
        decorated = retry_deco(max_tries=3)(self.mock_func)

        with patch('sys.stdout', new_callable=StringIO):
            result = decorated(1, 2, key="value")

        self.assertEqual(result, "success")
        self.mock_func.assert_called_once_with(1, 2, key="value")

    def test_retries_on_failure(self):
        self.mock_func.side_effect = [Exception("Error"), "success"]
        decorated = retry_deco(max_tries=2)(self.mock_func)

        with patch('sys.stdout', new_callable=StringIO):
            result = decorated()

        self.assertEqual(result, "success")
        self.assertEqual(self.mock_func.call_count, 2)

    def test_raises_after_max_attempts(self):
        self.mock_func.side_effect = Exception("Persistent error")
        decorated = retry_deco(max_tries=2)(self.mock_func)

        with patch('sys.stdout', new_callable=StringIO):
            with self.assertRaises(Exception) as context:
                decorated()

        self.assertEqual(str(context.exception), "Persistent error")
        self.assertEqual(self.mock_func.call_count, 2)

    def test_allowed_exception_immediately_raises(self):
        class AllowedError(Exception):
            pass

        self.mock_func.side_effect = AllowedError("Test")
        decorated = retry_deco(max_tries=3, check_exceptions=(AllowedError,))(self.mock_func)

        with patch('sys.stdout', new_callable=StringIO):
            with self.assertRaises(AllowedError):
                decorated()

        self.mock_func.assert_called_once()

    def test_print_output_format(self):
        self.mock_func.return_value = 42
        decorated = retry_deco(max_tries=1)(self.mock_func)

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            decorated("arg", key="value")
            output = mock_stdout.getvalue()

            self.assertIn(
                "run test_func with positional args=('arg',), with keyword kwargs={'key': 'value'}, attempt=1",
                output
            )
            self.assertIn("result=42", output)
