import unittest

from warnings import filterwarnings
from awsrdscli import isValidRegion
from awsrdscli import getRegionTypoRecommendation

class TestMethods(unittest.TestCase):

  def test_getRegionTypoRecommendation_positives(self):
    self.assertEqual(getRegionTypoRecommendation('ap-northeast-1a'), 'ap-northeast-1')
    self.assertEqual(getRegionTypoRecommendation('ap-northeast1-1'), 'ap-northeast-1')
    self.assertEqual(getRegionTypoRecommendation('ap1-northeast-1'), 'ap-northeast-1')
    self.assertEqual(getRegionTypoRecommendation('AP-NORTHEAST-1'), 'ap-northeast-1')

  def test_isValidRegion_positives(self):
    self.assertEqual(isValidRegion('ap-northeast-1'), 1)
    self.assertEqual(isValidRegion('ap-northeast-2'), 1)
    self.assertEqual(isValidRegion('ap-northeast-3'), 1)
    self.assertEqual(isValidRegion('ap-south-1'), 1)
    self.assertEqual(isValidRegion('ap-southeast-1'), 1)
    self.assertEqual(isValidRegion('ca-central-1'), 1)
    self.assertEqual(isValidRegion('eu-central-1'), 1)
    self.assertEqual(isValidRegion('eu-north-1'), 1)
    self.assertEqual(isValidRegion('eu-west-1'), 1)
    self.assertEqual(isValidRegion('eu-west-2'), 1)
    self.assertEqual(isValidRegion('eu-west-3'), 1)
    self.assertEqual(isValidRegion('sa-east-1'), 1)
    self.assertEqual(isValidRegion('us-east-1'), 1)
    self.assertEqual(isValidRegion('us-east-2'), 1)
    self.assertEqual(isValidRegion('us-west-1'), 1)
    self.assertEqual(isValidRegion('us-west-2'), 1)

  def test_isValidRegion_negatives(self):
    self.assertEqual(isValidRegion('ap-northeast-1a'), 0)
    self.assertEqual(isValidRegion('ap-northeast-10'), 0)
    self.assertEqual(isValidRegion('ap-northeast-a1'), 0)
    self.assertEqual(isValidRegion('ap-northeast-'), 0)
    self.assertEqual(isValidRegion('ap-northeast'), 0)
    self.assertEqual(isValidRegion('ap-northeasta-1'), 0)
    self.assertEqual(isValidRegion('ap1-northeast-1'), 0)
    self.assertEqual(isValidRegion('APNE1'), 0)
    self.assertEqual(isValidRegion('apne1'), 0)
    self.assertEqual(isValidRegion('AP-NORTHEAST-1'), 0)

  def setUp(self):
      filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")

if __name__ == '__main__':
  unittest.main()