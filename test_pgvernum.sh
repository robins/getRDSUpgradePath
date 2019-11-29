import unittest
import pgvernum

class TestMethods(unittest.TestCase):
    def test_add(self):
        self.assertEqual(pgvernum.getPGVersionString('9.3.14'), "90314")


if __name__ == '__main__':
    unittest.main()

#python pgvernum.py 9.3.14
# 90314
#py pgvernum.py 9.6.1
# 90601
#py pgvernum.py 10.0
# 100000
#py pgvernum.py 10.14
# 100014
#py pgvernum.py 11.1
# 110001