# This Python script uses boto3 so please ensure that is already installed
# and working in order, for this script to work as expected

import sys
import boto3

def callaws(arg, dest, engine):

  client = boto3.client('rds')

  # Ideally this takes non-postgres engines as well, although not well tested (XXX)
  resp = client.describe_db_engine_versions(
    Engine=engine,
    EngineVersion=arg,
  )

  # If there are no Upgrade paths, return right away
  if (not resp['DBEngineVersions']):
    return 0

  # Until caching comes in, process the list in reversed order (optimal)
  for k in reversed(resp['DBEngineVersions'][0]['ValidUpgradeTarget']):
    k2 = k['EngineVersion']
    if ((k2 == dest) or (callaws(k2, dest, engine) == 1)):
      print ('Upgrade From: ' + arg + ' To: ' + k2)
      return 1
  return 0

# Currently the default engine is postgres, unless explicitly provided (as 4th Option)
if len(sys.argv) == 3:
  engine = 'postgres'
elif len(sys.argv) == 4:
  engine = sys.argv[3]
else:
  print('Syntax: python getUpgradePath.py v1 v2 [engine]')
  print('Source / Destination Versions are Mandatory. You may also optionally mention Engine (default Postgres)')
  sys.exit()

if (callaws(sys.argv[1], sys.argv[2], engine) == 0):
  print("Unable to find Upgrade path")