import unittest
from weakref_slots import (
    Regular, WithSlots, WithWeakref,
    benchmark_create, benchmark_access,
    add, sub
)


class BenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.N = 10_000

    def test_regular_class(self):
        insts, t_create = benchmark_create(Regular, self.N)
        t_access = benchmark_access(insts)
        self.assertEqual(len(insts), self.N)
        self.assertGreater(t_create, 0)
        self.assertGreater(t_access, 0)

    def test_slots_class(self):
        insts, t_create = benchmark_create(WithSlots, self.N)
        t_access = benchmark_access(insts)
        self.assertEqual(len(insts), self.N)
        self.assertGreater(t_create, 0)
        self.assertGreater(t_access, 0)

    def test_weakref_class(self):
        insts, t_create = benchmark_create(WithWeakref, self.N)
        t_access = benchmark_access(insts)
        self.assertEqual(len(insts), self.N)
        self.assertGreater(t_create, 0)
        self.assertGreater(t_access, 0)

    def test_profile_decorator(self):
        add(10, 20)
        sub(30, 15)
        self.assertTrue(hasattr(add, 'print_stat'))
        self.assertTrue(hasattr(sub, 'print_stat'))


if __name__ == '__main__':
    unittest.main()
