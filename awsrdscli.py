import sys
import boto3

from textdistance import levenshtein

list = ['aurora-mysql', 'aurora-postgresql', 'aurora', 'docdb', 'mariadb', 'mysql', 'neptune', 'oracle-ee', 'postgres', 'sqlserver-ee', 'sqlserver-ex', 'sqlserver-se', 'sqlserver-web']

def isValidRDSEngine(s):

  if s in list:
    return 1
  else:
    return 0

def getRegionNames():
  # List all regions
  client = boto3.client('ec2')
  return [region['RegionName'] for region in client.describe_regions()['Regions']]

def isValidRegion(s):
  r = getRegionNames()
  if s in r:
    return 1
  else:
    return 0

# Ideally we should be checking for distance only when there is a spelling error
# (a.k.a. s not in list), but for an ad-hoc solution this doesn't hurt for now
def getRegionTypoRecommendation(s):
  r = getRegionNames()
  if (s.isupper()):
    s2=s.lower()
  else:
    s2 = s
  return min(r, key = lambda x: levenshtein(s2, x))

# Ideally we should be checking for distance only when there is a spelling error
# (a.k.a. s not in list), but for an ad-hoc solution this doesn't hurt for now
def getEngineTypoRecommendation(s):
  return min(list, key = lambda x: levenshtein(s, x))

# > aws rds describe-db-engine-versions | grep -w Engine | sed "s/^ *//;s/ *$//" | awk -F '"' '{print $4}' | sort | uniq
# aurora
# aurora-mysql
# aurora-postgresql
# docdb
# mariadb
# mysql
# neptune
# oracle-ee
# postgres
# sqlserver-ee
# sqlserver-ex
# sqlserver-se
# sqlserver-web

# > aws rds describe-db-engine-versions | grep -w Engine | sed "s/^ *//;s/ *$//" | awk -F '"' '{print $4}' | sort | uniq | wc -l
# 13

# >aws rds describe-source-regions | grep -w RegionName | awk -F "\"" "{print $4}"
# ap-northeast-1
# ap-northeast-2
# ap-northeast-3
# ap-south-1
# ap-southeast-1
# ca-central-1
# eu-central-1
# eu-north-1
# eu-west-1
# eu-west-2
# eu-west-3
# sa-east-1
# us-east-1
# us-east-2
# us-west-1
# us-west-2
