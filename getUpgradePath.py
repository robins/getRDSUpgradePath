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

import sys
import boto3
from pgvernum import getPGVersionString

lookup = {}
enable_caching = 1
allpaths = 0
debug = 0
soln = [[]]
src = sys.argv[1]
tgt = sys.argv[2]
cntargs = len(sys.argv)
engine='postgres'

def dexit(s):
  print (s)
  sys.exit(1)

def dprint(s):
  if (debug):
    print (s)

# Basic argument checks
def ensureArgumentChecks():
  if (cntargs < 3) or (cntargs > 5):
    print('Syntax: python getUpgradePath.py v1 v2 [engine] [mode]')
    print('Source / Destination Versions are Mandatory. You may also optionally mention Engine (default Postgres) and Mode (1 for Debug, 2 for All Upgrade Options, 3 for both Debug & All Upgrade Options)')
    sys.exit()
  elif cntargs == 3:
    # Unless provided, the default engine is postgres
    engine = 'postgres'
  elif cntargs >= 4:
    engine = sys.argv[3]

  # The last argument is for mode of operation
  if (cntargs == 5):
    if (sys.argv[4] == '1' or sys.argv[4] == '3'):
      debug = 1
    elif (sys.argv[4] >= '2'):
      allpaths = 1


def ensureVersionChecks():
  if (engine == 'postgres'):
    # Ensure the version strings are syntactically valid
    if (int(getPGVersionString(src)) < 0 or int(getPGVersionString(tgt) < 0)):
      dexit('Source / Destination Version string seem invalid')
    if ((getPGVersionString(src) > getPGVersionString(tgt))):
      dexit ('Skip upgrade check from newer to older version: ' + src + ' -> ' + tgt)
  if (not isVersionUpgradable(src, engine)):
    dexit("Unable to find Upgrade path. Is the Source version supported in RDS?")
  if (not isVersionUpgradable(tgt, engine)):
    dexit("Unable to find Upgrade path. Is the Target version supported in RDS?")


def isVersionUpgradable(ver, engine):
  dprint ('Checking Version: ' + ver)
  client = boto3.client('rds')
  resp = client.describe_db_engine_versions(
    Engine=engine,
    EngineVersion=ver,
  )
  upgrade_path=resp['DBEngineVersions']
  # Fail if there are no Upgrade paths
  if (not upgrade_path):
    return 0
  else:
    return upgrade_path


def findUpgradePaths(arg, dest, engine):
  upgrade_path = isVersionUpgradable(arg, engine)
  
  if (not upgrade_path):
    return 0
  
  k2 = []
  for k in reversed(upgrade_path[0]['ValidUpgradeTarget']):
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

    if ((k == dest) or (callaws(k, dest, engine, 0) == 1)):
      if (k == dest):
        print ("")
        print ("===============================")
      print ('Upgrade From: ' + arg + ' To: ' + k)
      return 1

  # If we reached here, it means this upgrade path isn't possible
  # We mark that and proceed with next possible combination
  v = arg + '-' + dest
  lookup[v] = -1
  return 0


def printUpgradePaths(src, tgt, engine):
  findUpgradePaths(src, tgt, engine)
  
  if (len(soln) == 0):
    dexit("Unable to find Upgrade path from " + src + ' to ' + tgt)
    
  for i in range(soln):
    print ()
    for j in range(i):
      print (j)
      if j == len(i):
        print ('->'),

# === Start ===

ensureArgumentChecks()
ensureVersionChecks()
printUpgradePaths(src, tgt, engine)
