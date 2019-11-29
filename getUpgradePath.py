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
from awsrdscli  import isValidRDSEngine

lookup = {}
enable_caching = 1
debug_level = -1  # User provided verbosity level. 5 => extremely verbose. 0 => quiet
debug_level_override = 0
default_debug_level = 1

def dexit(s, debug = default_debug_level):
  dprint(s, debug)
  sys.exit(1)

def dprint(s, debug = default_debug_level):
  if ((debug <= debug_level_override) or (debug <= debug_level)):
    print (s)

def cachelookup(src, tgt):
  v = src + '-' + tgt
  if (v in lookup):
    if (lookup[v] == 1):
      dprint ('Cache: Combination possible: ' + src + '-' + tgt, 3)
      return 1
    else:
      dprint ('Cache: Combination not possible: '  + src + '-' + tgt, 3)
      return 0
  else:
    dprint ('Cache: Combination not found: ' + src + '-' + tgt, 3)
    return -1

def callaws(src, tgt, engine):

  if (enable_caching):
    t = cachelookup(src, tgt)
    if (t >= 0):
      return t
  else:
    dprint('Caching disabled', 3)

  dprint('Calling AWS CLI with ' + src + ' ' + tgt + ' ' + engine, 2)
  client = boto3.client('rds')
  resp = client.describe_db_engine_versions(
    Engine=engine,
    EngineVersion=src
  )
  upgrade_path=resp['DBEngineVersions']
  # Fail if there are no Upgrade paths
  if (not upgrade_path):
    return 0
  else:
    return upgrade_path


def findUpgradePaths(src, tgt, engine):
  upgrade_path = callaws(src, tgt, engine)

  if (not upgrade_path):
    return 0

  k2 = []
  for k in reversed(upgrade_path[0]['ValidUpgradeTarget']):
    if (engine == 'postgres'):
      if ((getPGVersionString(k['EngineVersion']) > getPGVersionString(tgt))):
        dprint ('Skip upgrade check from newer to older version: ' + k['EngineVersion'] + ' -> ' + tgt, 3)
        continue

    k2.append(k['EngineVersion'])
    v = src + '-' + k['EngineVersion']
    if (not v in lookup):
      lookup[v] = 1

  dprint ('Valid targets: ' + '  '.join(k2), 4)
  dprint ('Cache: ' + '  '.join('(' + str(e) + '->' + str(lookup[e]) + ')' for e in lookup), 4)

  # Process the list in reversed order since ideally
  # the target is expected to be a recent Minor Version
  for k in (k2):

    if ((k == tgt) or (callaws(k, tgt, engine) == 1)):
      if (k == tgt):
        print ("")
        print ("===============================")
      print ('Upgrade From: ' + src + ' To: ' + k)
      return 1

  # If we reached here, it means this upgrade path isn't possible
  # We mark that and proceed with next possible combination
  v = src + '-' + tgt
  lookup[v] = -1
  return 0


def validateCLIArgsOrFail():
  global debug_level
  d = dict()

  # Basic bash argument count check
  if ((len(sys.argv) < 3) or (len(sys.argv) > 5)):
    print('Syntax: python getUpgradePath.py v1 v2 [engine] [DebugLevel]')
    print("""Source / Target Versions are Mandatory. Optionally, you may also provide:
  Engine: (default 'postgres')
  DebugLevel: (default '1')""")
    sys.exit()

  # The last argument is for mode of operation
  if (len(sys.argv) == 5):
    debug_level = int(sys.argv[4])
    if (int(debug_level) < 0 & int(debug_level) > 5):
      print("Invalid Debug Level: " + debug_level)
      sys.exit()
  else:
    debug_level = default_debug_level

  dprint("Arg array: " + ','.join(sys.argv[1:]), 5)
  dprint("argv length: "+ str(len(sys.argv)), 5)
  dprint("Arg 0: " + str(sys.argv[0]), 5)
  dprint("Arg 1: " + str(sys.argv[1]), 5)
  dprint("Arg 2: " + str(sys.argv[2]), 5)
  if (len(sys.argv) >=4): dprint("Arg 3: " + str(sys.argv[3]), 5)
  if (len(sys.argv) >=5): dprint("Arg 4: " + str(sys.argv[4]), 5)

  dprint("Debug Level: " + str(debug_level), 4)

  # Validate the engine provided (If not provided the default is postgres)
  if len(sys.argv) >= 4:
    d['engine'] = sys.argv[3]
    if isValidRDSEngine(d['engine']):
      dexit('Invalid Engine: ' + d['engine'])
  elif len(sys.argv) == 3:
    d['engine'] = 'postgres'

  dprint("Engine: " + d['engine'], 4)

  d['src'] = sys.argv[1]
  d['tgt'] = sys.argv[2]

  if (d['src'] == d['tgt']):
    dexit("No upgrade required when Source and Target versions are the same")

  # Try to validate syntactic validity without calling AWS CLI, if possible
  if (d['engine'] == 'postgres'):
    if (int(getPGVersionString(d['src']))<0):
      dexit('Source Engine Version is invalid: ' + d['src'])
    if (int(getPGVersionString(d['tgt']) < 0)):
      dexit('Target Engine Version is invalid: ' + d['tgt'])
    if ((getPGVersionString(d['src']) > getPGVersionString(d['tgt']))):
      dexit ('Cannot upgrade from newer to older version: ' + d['src'] + ' -> ' + d['tgt'])

  # We've already done basic check on version numbers, so an error here may not
  # necessarily mean an invalid version. It's possible it isn't supported in RDS (yet)
  if (callaws(d['src'], 'x', d['engine']) == 0):
    dexit("Source Engine Version is not supported in RDS: " + d['src'])
  if (callaws(d['tgt'], 'y', d['engine']) == 0):
    dexit("Target Engine Version is not supported in RDS: " + d['tgt'])

  dprint("Source Version: " + d['src'], 4)
  dprint("Target Version: " + d['tgt'], 4)

  return d

def getUpgradePathForCombination(src, tgt, engine):
  if (callaws(d['src'], d['tgt'], d['engine'], 0) == 0):
    print ('')
    print ("===============================")
    print("Unable to find Upgrade path from " + sys.argv[1] + ' to ' + sys.argv[2])

  print ("===============================")

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

d = dict()
d = validateCLIArgsOrFail()
printUpgradePaths(d['src'], d['tgt'], d['engine'])