import sys
import boto3

lookup.clear()

def callaws(arg, dest, engine):

  if (get(d[arg]) == None):
    resp = client.describe_db_engine_versions(
      Engine=engine,
      EngineVersion=arg,
    )

    if (len(resp['DBEngineVersions'][0]['ValidUpgradeTarget']) == 0):
      return 0

    for k in resp['DBEngineVersions'][0]['ValidUpgradeTarget']:
      

  for k in reversed(resp['DBEngineVersions'][0]['ValidUpgradeTarget']):
    k2 = k['EngineVersion']
    if ((k2 == dest) or (callaws(k2, dest, engine) == 1)):
      print ('From: ' + arg + ' To:' + k2)
      return 1
      
if not (len(sys.argv) >= 3 and len(sys.argv) <= 4):
  print('Syntax: python getUpgradePath.py v1 v2 [engine]')
  print('Source / Destination Versions are Mandatory. You may also optionally mention Engine (default Postgres)')
  sys.exit()

client= boto3.client('rds')
if len(sys.argv) == 3:
  engine = 'postgres'

if (callaws(sys.argv[1], sys.argv[2], engine) == 0):
  print("Unable to find Upgrade path")