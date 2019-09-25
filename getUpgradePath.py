# This Python script uses boto3 so please ensure that is already installed
# and working in order, for this script to work as expected

import sys
import boto3

lookup = {}

def callaws(arg, dest, engine, just_check):

  print ('============')
  print ('Checking combination ' + arg + '-' + dest)

  v = arg + '-' + dest
  if (v in lookup):
    if (lookup[v] == 1):
      print ('Cached: Combination possible')
      return 1
    else:
      print ('Cached: Combination not possible')
      return 0

  client = boto3.client('rds')

  # Ideally this takes non-postgres engines as well, although not well tested (XXX)
  resp = client.describe_db_engine_versions(
    Engine=engine,
    EngineVersion=arg,
  )

  # If there are no Upgrade paths, return right away
  if (not resp['DBEngineVersions']):
    return 0

  if (just_check):
    return 1

  k2 = []
  for k in reversed(resp['DBEngineVersions'][0]['ValidUpgradeTarget']):
    k2.append(k['EngineVersion'])
    v = arg + '-' + k['EngineVersion']
    if (not v in lookup):
      lookup[v] = 1

  print ('Valid targets: ' + '  '.join(k2))
  print ('Lookup: ' + '  '.join(lookup))

  # Process the list in reversed order since ideally 
  # the target is expected to be a recent Minor Version
  for k in (k2):
    if ((k == dest) or (callaws(k, dest, engine, 0) == 1)):
      print ('Upgrade From: ' + arg + ' To: ' + k)
      return 1

  v = arg + '-' + dest
  lookup[v] = -1
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

if (callaws(sys.argv[1], 'x', engine, 1) == 0):
  print("Unable to find Upgrade path. Is the Source version supported in RDS?")
  sys.exit() 

if (callaws(sys.argv[2], 'y', engine, 1) == 0):
  print("Unable to find Upgrade path. Is the Target version supported in RDS?")
  sys.exit()

if (callaws(sys.argv[1], sys.argv[2], engine, 0) == 0):
  print("Unable to find Upgrade path")
