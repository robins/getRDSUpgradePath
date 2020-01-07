import unittest

from warnings import filterwarnings
from getUpgradePath import main

class TestMethods(unittest.TestCase):
  def test_main(self):
    self.assertEqual(main(['getUpgradePath.py', '9.4.23','9.5.15', 'postgres', '1', '0']), "Upgrade path not found")
    self.assertEqual(main(['getUpgradePath.py', '9.3.14','9.3.16', 'postgres', '1', '0']), "['9.3.14', '9.3.16']")
    self.assertEqual(main(['getUpgradePath.py', '9.4.23','9.5.18', 'postgres', '1', '0']), "['9.4.23', '9.5.18']")

  def setUp(self):
      filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")

if __name__ == '__main__':
  unittest.main()