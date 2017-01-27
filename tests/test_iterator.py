import unittest
from syntax_sugar.iterator import *
from itertools import product
from random import randint

class TestIterator(unittest.TestCase):
    def test_valid_init(self):
        self.assertIsInstance(Iterator(0, INF), Iterator)
        self.assertIsInstance(Iterator(0, INF, 3), Iterator)
        self.assertIsInstance(Iterator(40, 1000, 32), Iterator)
        self.assertIsInstance(Iterator(500, 20), Iterator)
        self.assertIsInstance(Iterator(4000, 75, -90), Iterator)

    def test_type_error_init(self):
        with self.assertRaises(TypeError): Iterator(1, 'a')
        with self.assertRaises(TypeError): Iterator('a', 1)
        with self.assertRaises(TypeError): Iterator('ntoeuh', 'z')
        with self.assertRaises(TypeError): Iterator([1], [2])

    def test_value_error_init(self):
        with self.assertRaises(ValueError): Iterator(INF, 2)
        with self.assertRaises(ValueError): Iterator(INF, 'z')
        with self.assertRaises(ValueError): Iterator(1, 10, 0)
        with self.assertRaises(ValueError): Iterator(1, 10, -1)
        with self.assertRaises(ValueError): Iterator(10, 1, 0)
        with self.assertRaises(ValueError): Iterator(10, 1, 1)
        with self.assertRaises(ValueError): Iterator('a', 'z', 0)
        with self.assertRaises(ValueError): Iterator('a', 'z', -1)
        with self.assertRaises(ValueError): Iterator('z', 'a', 0)
        with self.assertRaises(ValueError): Iterator('z', 'a', 1)

    def test_generated_values(self):
        self.assertEqual(list(range(1, 11)), list(Iterator(1, 10)))
        self.assertEqual(list(range(5, 501, 7)), list(Iterator(5, 500, 7)))
        self.assertEqual(list(range(10, 0, -1)), list(Iterator(10, 1)))
        self.assertEqual(list(range(500, 4, -7)), list(Iterator(500, 5, -7)))
        self.assertEqual("abcdef", str(Iterator('a', 'f')))
        self.assertEqual("fedcba", str(Iterator('f', 'a')))
        self.assertEqual("DFHJLNPRTV", str(Iterator('D', 'V', 2)))
        self.assertEqual("VTRPNLJHFD", str(Iterator('V', 'D', -2)))

    def test_multiplication_operator(self):
        self.assertEqual(
                list(Iterator(1, 3) * Iterator(3, 1)),
                list(product(range(1, 4), range(3, 0, -1))))

        def vals_and_step():
            value_1, value_2 = randint(1, 100), randint(1, 100)
            step = 1 if value_1 < value_2 else -1
            return (value_1, value_2, step)

        for i in range(50):
            start_1, end_1, step_1 = vals_and_step()
            start_2, end_2, step_2 = vals_and_step()

            asc = Iterator(start_1, end_1, step_1)
            desc = Iterator(start_2, end_2, step_2)

            v_product_range = product(
                    range(start_1, end_1 + step_1, step_1),
                    range(start_2, end_2 + step_2, step_2))

            self.assertEqual(list(asc * desc), list(v_product_range))
