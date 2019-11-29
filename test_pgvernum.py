import unittest
import pgvernum

class TestMethods(unittest.TestCase):
    def test_add(self):
        self.assertEqual(pgvernum.getPGVersionString('9.3.14'), 90314)
        self.assertEqual(pgvernum.getPGVersionString('9.6.1'), 90601)
        self.assertEqual(pgvernum.getPGVersionString('10.0'), 100000)
        self.assertEqual(pgvernum.getPGVersionString('10.14'), 100014)
        self.assertEqual(pgvernum.getPGVersionString('11.1'), 110001)

if __name__ == '__main__':
    unittest.main()