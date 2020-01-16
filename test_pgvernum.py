import unittest
import pgvernum

class TestMethods(unittest.TestCase):
  def test_getPGVerNumFromString(self):
    self.assertEqual(pgvernum.getPGVerNumFromString('9.3.14'), 90314)
    self.assertEqual(pgvernum.getPGVerNumFromString('9.6.1'), 90601)
    self.assertEqual(pgvernum.getPGVerNumFromString('10.0'), 100000)
    self.assertEqual(pgvernum.getPGVerNumFromString('10.14'), 100014)
    self.assertEqual(pgvernum.getPGVerNumFromString('11.1'), 110001)
    self.assertEqual(pgvernum.getPGVerNumFromString('9.3.14'), 90314)
    self.assertEqual(pgvernum.getPGVerNumFromString('11.9999'), 119999)
    self.assertEqual(pgvernum.getPGVerNumFromString('9.3.99'), 90399)
    self.assertEqual(pgvernum.getPGVerNumFromString('9.99.1'), 99901)

  def test_getPGVersionString_negatives(self):
    self.assertEqual(pgvernum.getPGVerNumFromString('9'), 0)
    self.assertEqual(pgvernum.getPGVerNumFromString('9.6'), 0)
    self.assertEqual(pgvernum.getPGVerNumFromString('10'), 0)
    self.assertEqual(pgvernum.getPGVerNumFromString('9.3.1.1'), 0)
    self.assertEqual(pgvernum.getPGVerNumFromString('10.1.1'), 0)
    self.assertEqual(pgvernum.getPGVerNumFromString('9.3.1a'), 0)
    self.assertEqual(pgvernum.getPGVerNumFromString('10.1b'), 0)

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
    self.assertEqual(pgvernum.isValidPGVersion('11.10000'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('9.6.100'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('9.100.10'), 0)
    self.assertEqual(pgvernum.isValidPGVersion('#'), 0)

  def test_isValidPGVersion_positives(self):
    self.assertEqual(pgvernum.isValidPGVersion('9.3.0'), 1)
    self.assertEqual(pgvernum.isValidPGVersion('11.1'), 1)

  def test_getMajorPGVersion_positives(self):
    self.assertEqual(pgvernum.getMajorPGVersion('9.3'), 9.3)
    self.assertEqual(pgvernum.getMajorPGVersion('9.3.0'), 9.3)
    self.assertEqual(pgvernum.getMajorPGVersion('11.1'), 11)
    self.assertEqual(pgvernum.getMajorPGVersion('11.0'), 11)
    self.assertEqual(pgvernum.getMajorPGVersion('11'), 11)

  def test_getMajorPGVersion_negatives(self):
    self.assertLess(pgvernum.getMajorPGVersion('9'), 0)
    self.assertLess(pgvernum.getMajorPGVersion('11.2.2'), 0)
    self.assertLess(pgvernum.getMajorPGVersion('a'), 0)

  def test_getMinorPGVersion_positives(self):
    self.assertEqual(pgvernum.getMinorPGVersion('9.3.0'), 0)
    self.assertEqual(pgvernum.getMinorPGVersion('11.1'), 1)

  def test_getMinorPGVersion_negatives(self):
    self.assertLess(pgvernum.getMinorPGVersion('9.3'), 0)
    self.assertLess(pgvernum.getMinorPGVersion('11'), 0)

  def test_parsePGVersion_positives(self):
    self.assertEqual(pgvernum.parsePGVersion('9.3.0'), [9.3, 0])
    self.assertEqual(pgvernum.parsePGVersion('11.1'), [11,1])

  def test_parsePGVersion_negatives(self):
    self.assertLess(pgvernum.parsePGVersion('9.3'), 0)
    self.assertLess(pgvernum.parsePGVersion('11'), 0)

  def test_appendMinorVersionIfRequired_positives(self):
    self.assertEqual(pgvernum.appendMinorVersionIfRequired('9.3'), '9.3.0')
    self.assertEqual(pgvernum.appendMinorVersionIfRequired('11'), '11.0')

  def test_appendMinorVersionIfRequired_negatives(self):
    self.assertEqual(pgvernum.appendMinorVersionIfRequired('9.3.2'), '9.3.2')
    self.assertEqual(pgvernum.appendMinorVersionIfRequired('11.1a'), '11.1a')

  def test_getVerReleasedDate_positives(self):
    self.assertEqual(pgvernum.getVerReleasedDate('12.1'), '2019-11-14')
    self.assertEqual(pgvernum.getVerReleasedDate('12.0'), '2019-10-03')
    self.assertEqual(pgvernum.getVerReleasedDate('10.1'), '2017-11-09')

  def test_getVerReleasedDate_negatives(self):
    self.assertEqual(pgvernum.getVerReleasedDate('12.100'), '0')
    self.assertEqual(pgvernum.getVerReleasedDate('12.'), '0')
    self.assertEqual(pgvernum.getVerReleasedDate('12.a'), '0')
    self.assertEqual(pgvernum.getVerReleasedDate('1232'), '0')
    self.assertEqual(pgvernum.getVerReleasedDate('-1'), '0')

  def test_IsVerReleasedAfter_positives(self):
    self.assertEqual(pgvernum.IsVerReleasedAfter('12.1', '11.5'), 1)
    self.assertEqual(pgvernum.IsVerReleasedAfter('9.4.23', '9.5.15'), 1)
    self.assertEqual(pgvernum.IsVerReleasedAfter('12.0', '12.1'), 0)
    self.assertEqual(pgvernum.IsVerReleasedAfter('12.1', '11.6'), 0)

  def test_IsVerReleasedAfter_negatives(self):
    self.assertEqual(pgvernum.IsVerReleasedAfter('121', '12.0'), 0)
    self.assertEqual(pgvernum.IsVerReleasedAfter('121', '120'), 0)
    self.assertEqual(pgvernum.IsVerReleasedAfter('12.1', '120'), 0)
    self.assertEqual(pgvernum.IsVerReleasedAfter('12.1', 'a'), 0)
    self.assertEqual(pgvernum.IsVerReleasedAfter('12.1', ''), 0)
    self.assertEqual(pgvernum.IsVerReleasedAfter('12.1', '#'), 0)
    self.assertEqual(pgvernum.IsVerReleasedAfter('12.1', '.'), 0)
    self.assertEqual(pgvernum.IsVerReleasedAfter('12.1', '..'), 0)
    self.assertEqual(pgvernum.IsVerReleasedAfter('12.1', '...'), 0)
    self.assertEqual(pgvernum.IsVerReleasedAfter('a', '12.0'), 0)
    self.assertEqual(pgvernum.IsVerReleasedAfter('', '12.0'), 0)
    self.assertEqual(pgvernum.IsVerReleasedAfter('.', '12.0'), 0)
    self.assertEqual(pgvernum.IsVerReleasedAfter('..', '12.0'), 0)
    self.assertEqual(pgvernum.IsVerReleasedAfter('...', '12.0'), 0)
    self.assertEqual(pgvernum.IsVerReleasedAfter('#', '12.0'), 0)

if __name__ == '__main__':
  unittest.main(failfast=True)