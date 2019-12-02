import unittest

from getUpgradePath import main

class TestMethods(unittest.TestCase):
  def test_main(self):
    self.assertEqual(main(['getUpgradePath.py', '9.3.14','9.3.16', 'postgres', '1', '0']), 90314)

if __name__ == '__main__':
  unittest.main()