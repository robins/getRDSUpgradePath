# This Python script uses boto3 so please ensure that is already installed
# and working in order, for this script to work as expected

# Further, note that this script returns the first successful combination
# and doesn't yet make an effort to do an exhaustive search on the "best"
# combination based on effort required (to upgrade) / compatibilities / 
# efficiency / speed of upgrade etc. It does try to optimize a little in that
# it tries to do a reverse search of upgrade paths possible, but it is quite
# possible that an alternate path of upgrade had less upgrade steps.

# In essence this is possibly a travelling saleman problem, and without an
# exhaustive search it is impossible to rule out whether a faster combination
# is possible. This is a to-do item here, but hasn't been implemented yet.

# 

import sys
import boto3
from pgvernum import getPGVersionString

lookup = {}
enable_caching = 1
allpaths = 0
debug = 0

def dexit(s):
  print (s)
  sys.exit(1)
    
def dprint(s):
  if (debug):
    print (s)

def callaws(arg, dest, engine, just_check):

  dprint ('')
  dprint ('Checking combination ' + arg + '-' + dest)

  v = arg + '-' + dest
  if ((enable_caching) and (v in lookup)):
    if (lookup[v] == 1):
      dprint ('Cache: Combination possible')
      return 1
    else:
      dprint ('Cache: Combination ' + arg + '->' + dest + ' not possible')
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
    if (engine == 'postgres'):
      if ((getPGVersionString(k['EngineVersion']) > getPGVersionString(dest))):
        dprint ('Skip upgrade check from newer to older version: ' + k['EngineVersion'] + ' -> ' + dest)
        continue

    k2.append(k['EngineVersion'])
    v = arg + '-' + k['EngineVersion']
    if (not v in lookup):
      lookup[v] = 1

  dprint ('Valid targets: ' + '  '.join(k2))
  dprint ('Cache: ' + '  '.join('(' + str(e) + '->' + str(lookup[e]) + ')' for e in lookup))

  # Process the list in reversed order since ideally 
  # the target is expected to be a recent Minor Version
  for k in (k2):

#    if (engine == 'postgres'):

      # Assuming that the program wouldn't generate (or the CLI wouldn't return) an
      # invalid PG Version number: XXX
#      if (abs(getPGVersionString(arg) - getPGVersionString(dest)) < 100):
#        dprint ('We''re unnecessarily doing a minor version jump. Skip it')
#        continue

    if ((k == dest) or (callaws(k, dest, engine, 0) == 1)):
      if (k == dest):
        print ("")
        print ("===============================")
      print ('Upgrade From: ' + arg + ' To: ' + k)
      return 1

  # We keep an impossible set (denoted by -1), since we can't 
  # 'optimize' this out owing to how pre v10 versions weren't 
  # simple string comparisons for e.g. unless we use Postgres' 
  # way of converting versions like v9.6.8 to an integer, 
  # we can't know which came later between v9.6.8 and v10.1
  v = arg + '-' + dest
  lookup[v] = -1
  return 0

# Currently the default engine is postgres, unless explicitly provided (as 4th Option)
if len(sys.argv) >= 4:
  engine = sys.argv[3]

if len(sys.argv) == 3:
  engine = 'postgres'

if (engine == 'postgres'):
  if (int(getPGVersionString(sys.argv[1])) < 0 or int(getPGVersionString(sys.argv[2]) < 0)):
    dexit('Source / Destination Version string seem invalid')
  if ((getPGVersionString(sys.argv[1]) > getPGVersionString(sys.argv[2]))):
    dexit ('Don''t need to check if we can upgrade from newer to older version: ' + sys.argv[1] + ' -> ' + sys.argv[2])

if ((len(sys.argv) < 3) or (len(sys.argv) > 5)):
  print('Syntax: python getUpgradePath.py v1 v2 [engine] [mode]')
  print('Source / Destination Versions are Mandatory. You may also optionally mention Engine (default Postgres) and Mode (1 for Debug, 2 for All Upgrade Options, 3 for both Debug & All Upgrade Options)')
  sys.exit()

if (callaws(sys.argv[1], 'x', engine, 1) == 0):
  print("Unable to find Upgrade path. Is the Source version supported in RDS?")
  sys.exit() 

if (callaws(sys.argv[2], 'y', engine, 1) == 0):
  print("Unable to find Upgrade path. Is the Target version supported in RDS?")
  sys.exit()

# The last argument is for mode of operation
if (len(sys.argv) == 5):
  if (sys.argv[4] == '1' or sys.argv[4] == '3'):
    debug = 1
  elif (sys.argv[4] == '2'):
    allpaths = 1

if (callaws(sys.argv[1], sys.argv[2], engine, 0) == 0):
  print ('')
  print ("===============================")
  print("Unable to find Upgrade path from " + sys.argv[1] + ' to ' + sys.argv[2])
  print ("===============================")
else:
  print ("===============================")