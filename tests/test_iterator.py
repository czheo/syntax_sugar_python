import unittest
from syntax_sugar.iterator import *

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
