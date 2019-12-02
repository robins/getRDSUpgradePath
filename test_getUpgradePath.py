import unittest
import getUpgradePath

class TestMethods(unittest.TestCase):
  def test_getPGVersionString(self):
    self.assertEqual(pgvernum.getPGVersionString('9.3.14'), 90314)
    self.assertEqual(pgvernum.getPGVersionString('9.6.1'), 90601)
    self.assertEqual(pgvernum.getPGVersionString('10.0'), 100000)
    self.assertEqual(pgvernum.getPGVersionString('10.14'), 100014)
    self.assertEqual(pgvernum.getPGVersionString('11.1'), 110001)
    self.assertEqual(pgvernum.getPGVersionString('9.3.14'), 90314)

  def test_getPGVersionString_negatives(self):
    self.assertEqual(pgvernum.getPGVersionString('9.3'), 0)
    self.assertEqual(pgvernum.getPGVersionString('9.3.1.1'), 0)
    self.assertEqual(pgvernum.getPGVersionString('9.3.1a'), 0)
    self.assertEqual(pgvernum.getPGVersionString('10'), 0)
    self.assertEqual(pgvernum.getPGVersionString('9'), 0)
    self.assertEqual(pgvernum.getPGVersionString('10.1.1'), 0)
    self.assertEqual(pgvernum.getPGVersionString('10.1b'), 0)
    self.assertEqual(pgvernum.getPGVersionString('10'), 0)

  def test_isValidPGVersion_negatives(self):
    self.assertEqual(pgvernum.isValidPGVersion(''), 0)
    self.assertEqual(pgvernum.isValidPGVersion('a'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('a.a'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('a.a.a'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('.'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('..'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('...'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('1'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('9'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('9.4'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('.9.4'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('9.4.'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('94'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('9.4.4.4.4'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('9b.2.4'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('b9.2.12'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('b.2.2'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('9.b2.12'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('9.2b.12'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('9.b.12'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('9.2.b12'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('9.2.12b'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('9.2.b'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('-9.3.1'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('11.1.1'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('11.1.'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('11.1a'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('11.a1'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('11.a'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('11a.1'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('a11.1'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('9..'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('9..1'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('11..'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('11.'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('11.1.'), 0)

  def test_isValidPGVersion_positives(self):
    self.assertEqual(pgvernum.isValidPGVersion('9.3.0'), 1)
    self.assertEqual(pgvernum.isValidPGVersion('11.1'), 1)

if __name__ == '__main__':
  unittest.main()