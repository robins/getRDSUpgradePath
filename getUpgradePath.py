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
    return 0

def callaws(arg, tgt, engine, just_check):

  if (enable_caching):
    if (cachelookup(arg, tgt)):
      return 1
  else:
    dprint('Caching disabled', 2)

  dprint('Calling AWS CLI with ' + arg + ' ' + tgt + ' ' + engine, 2)
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
      if ((getPGVersionString(k['EngineVersion']) > getPGVersionString(tgt))):
        dprint ('Skip upgrade check from newer to older version: ' + k['EngineVersion'] + ' -> ' + tgt, 3)
        continue

    k2.append(k['EngineVersion'])
    v = arg + '-' + k['EngineVersion']
    if (not v in lookup):
      lookup[v] = 1

  dprint ('Valid targets: ' + '  '.join(k2), 4)
  dprint ('Cache: ' + '  '.join('(' + str(e) + '->' + str(lookup[e]) + ')' for e in lookup), 4)

  # Process the list in reversed order since ideally
  # the target is expected to be a recent Minor Version
  for k in (k2):

    if ((k == tgt) or (callaws(k, tgt, engine, 0) == 1)):
      if (k == tgt):
        print ("")
        print ("===============================")
      print ('Upgrade From: ' + arg + ' To: ' + k)
      return 1

  # If we reached here, it means this upgrade path isn't possible
  # We mark that and proceed with next possible combination
  v = arg + '-' + tgt
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
  if (callaws(d['src'], 'x', d['engine'], 1) == 0):
    dexit("Source Engine Version is not yet supported in RDS: " + d['src'])
  if (callaws(d['tgt'], 'y', d['engine'], 1) == 0):
    dexit("Target Engine Version is not yet supported in RDS: " + d['tgt'])

  dprint("Source Version: " + d['src'], 4)
  dprint("Target Version: " + d['tgt'], 4)

  return d

def getUpgradePathForCombination(src, tgt, engine):
  if (callaws(d['src'], d['tgt'], d['engine'], 0) == 0):
    print ('')
    print ("===============================")
    print("Unable to find Upgrade path from " + sys.argv[1] + ' to ' + sys.argv[2])

  print ("===============================")


d = dict()
d = validateCLIArgsOrFail()
getUpgradePathForCombination(d['src'], d['tgt'], d['engine'])