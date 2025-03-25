import unittest

from retry_deco import retry_deco


class TestRetryDeco(unittest.TestCase):

    def test_add_success(self):
        @retry_deco(3)
        def add(a, b):
            return a + b

        result = add(4, 2)
        self.assertEqual(result, ((4, 2), {}, 1, 6))

        result = add(4, b=3)
        self.assertEqual(result, ((4,), {'b': 3}, 1, 7))

    def test_check_str_success(self):
        @retry_deco(3)
        def check_str(value=None):
            if value is None:
                raise ValueError()
            return isinstance(value, str)

        result = check_str(value="123")
        self.assertEqual(result, ((), {'value': '123'}, 1, True))

        result = check_str(value=1)
        self.assertEqual(result, ((), {'value': 1}, 1, False))

    def test_check_str_failure(self):
        @retry_deco(3)
        def check_str(value=None):
            if value is None:
                raise ValueError()
            return isinstance(value, str)

        result = check_str(value=None)
        *answer, exc = result
        self.assertIsInstance(exc, ValueError)

        self.assertEqual(answer, [(), {'value': None}, 3])

    def test_check_int_success(self):
        @retry_deco(2, [ValueError])
        def check_int(value=None):
            if value is None:
                raise ValueError()
            return isinstance(value, int)

        result = check_int(value=1)
        self.assertEqual(result, ((), {'value': 1}, 1, True))

    def test_check_int_failure(self):
        @retry_deco(2, [ValueError])
        def check_int(value=None):
            if value is None:
                raise ValueError()
            return isinstance(value, int)

        result = check_int(value=None)
        *answer, exc = result
        self.assertIsInstance(exc, ValueError)
        self.assertEqual(answer, [(), {'value': None}, 1])
