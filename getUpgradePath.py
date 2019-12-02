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
import re
import time

from pgvernum import getPGVersionString
from pgvernum import appendMinorVersionIfRequired
from awsrdscli import isValidRDSEngine
from awsrdscli import getEngineTypoRecommendation

lookup = {} # 1-step upgrade paths + a flag for whether they are possible
soln = [] # All steps of (only successful) upgrade paths (from src to tgt)
enable_caching = 1
hops_desired = 1
debug_level = -1  # User provided verbosity level. 5 => extremely verbose. 0 => quiet
debug_level_override = 0
default_debug_level = 1

def dexit(s, debug = default_debug_level):
  dprint(s, debug)
  sys.exit(1)

def dprint(s, debug = default_debug_level):
  if ((debug <= debug_level_override) or (debug <= debug_level)):
    print (s)

def validateCLIArgsOrFail(argv):
  global debug_level, hops_desired
  d = dict()

  # Basic bash argument count check
  if ((len(argv) < 3) or (len(argv) > 6)):
    print("""
Syntax: python getUpgradePath.py SourceVersion TargetVersion [engine] [hops] [verbosity]

Source / Target Versions are Mandatory. Optionally, you may also provide:
  Engine: RDS Database Engine | Default:postgres
  Hops: Find all upgrade combinations possible within these many Hops | Default:1 | Range:1-10
  Verbosity: Verbosity of the output | Default:1 | Range:1-5""")
    sys.exit()

  # The last argument is for Debug Level
  if (len(argv) == 6):
    debug_level = int(argv[5])
    if (int(debug_level) < 0 or int(debug_level) > 6):
      print("Invalid Verbosity level: " + str(debug_level))
      print("Hint: Verbosity level ranges from 1-5")
      sys.exit()
  else:
    debug_level = default_debug_level

  # The last argument is for Debug Level
  if (len(argv) >= 5):
    hops_desired = int(argv[4])
    if (int(hops_desired) < 1 or int(hops_desired) > 10):
      print("Invalid Hop level: " + str(debug_level))
      print("Hint: Hop level ranges from 1-10")
      sys.exit()

  dprint("Arg array: " + ','.join(argv[1:]), 5)
  dprint("argv length: "+ str(len(argv)), 5)
  dprint("Arg 0: " + str(argv[0]), 5)
  dprint("Arg 1: " + str(argv[1]), 5)
  dprint("Arg 2: " + str(argv[2]), 5)
  if (len(argv) >=4): dprint("Arg 3: " + str(argv[3]), 5)
  if (len(argv) >=5): dprint("Arg 4: " + str(argv[4]), 5)

  dprint("Debug Level: " + str(debug_level), 4)

  # Validate the engine provided (If not provided the default is postgres)
  if len(argv) >= 4:
    d['engine'] = argv[3]
    if not isValidRDSEngine(d['engine']):
      dprint('Invalid Engine: ' + d['engine'])
      dprint("Hint: May be you meant - " + getEngineTypoRecommendation(d['engine']))
      sys.exit()
  elif len(argv) == 3:
    d['engine'] = 'postgres'

  dprint("Engine: " + d['engine'], 4)

  d['src'] = argv[1]
  d['tgt'] = argv[2]

  if (d['src'] == d['tgt']):
    dexit("No upgrade required when Source and Target versions are the same")

  # Try to validate syntactic validity without calling AWS CLI, if possible
  if (d['engine'] == 'postgres'):

    if (d['src'] != appendMinorVersionIfRequired(d['src'])):
      d['src'] = appendMinorVersionIfRequired(d['src'])
      dprint("Source Version corrected to - " + d['src'])

    if (d['tgt'] != appendMinorVersionIfRequired(d['tgt'])):
      d['tgt'] = appendMinorVersionIfRequired(d['tgt'])
      dprint("Target Version corrected to - " + d['tgt'])

    if (int(getPGVersionString(d['src'])) == 0):
      dexit('Source Engine Version is invalid: ' + d['src'])
    if (int(getPGVersionString(d['tgt']) == 0)):
      dexit('Target Engine Version is invalid: ' + d['tgt'])
    if ((getPGVersionString(d['src']) >= getPGVersionString(d['tgt']))):
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

def cachelookup(src, tgt):
  if (src in lookup):
    if (tgt in lookup[src]):
      if (lookup[src][tgt] == 1):
        dprint ('Cache: Combination possible: ' + src + '->' + tgt, 3)
        return 1
      else:
        dprint ('Cache: Combination not possible: '  + src + '->' + tgt, 3)
        return 0
  dprint ('Cache: Combination not found: ' + src + '->' + tgt, 3)
  return -1

def callaws(src, tgt, engine):

  dprint('Calling AWS CLI with ' + src + ' ' + tgt + ' ' + engine, 2)
  client = boto3.client('rds')

  # Sample CLI: aws rds describe-db-engine-versions --engine=postgres --engine-version=9.3.12
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

def findAdjacentUpgrades(src, tgt, engine):
  global lookup

  if (enable_caching):
    t = cachelookup(src, tgt)
    if (t >= 0):
      return
  else:
    dprint('Caching disabled', 3)

  upgrade_path = callaws(src, tgt, engine)

  if (not upgrade_path):
    if not (src in lookup):
      lookup[src]={}
    lookup[src][tgt] = 1000
    return

  k2 = []
  # print (str(upgrade_path))
  for k in reversed(upgrade_path[0]['ValidUpgradeTarget']):

    # Avoid CLI calls if possible
    if (engine == 'postgres'):
      if ((getPGVersionString(k['EngineVersion']) >= getPGVersionString(tgt))):
        dprint ('Skip upgrade check from newer to older version: ' + k['EngineVersion'] + ' -> ' + tgt, 3)
        continue

    k2.append(k['EngineVersion'])
    if not (src in lookup):
      lookup[src]={}
    lookup[src][k['EngineVersion']] = 1

  dprint ('Valid targets: ' + '  '.join(k2), 4)
  dprint ('Cache: ' + "\n".join('(' + str(e) + '->' + str(lookup[e]) + ')' for e in lookup), 4)

  # Process the list in reversed order since ideally
  # the target is expected to be a recent Minor Version
  for k in (k2):
    if not (k == tgt):
      findAdjacentUpgrades(k, tgt, engine)

  # If we reached here, it means this upgrade path isn't possible
  # We mark that and proceed with next possible combination
  if not (src in lookup):
    lookup[src]={}
  if not (tgt in lookup[src]):
    lookup[src][tgt] = 1002
  return

def createtraversalmatrix(src, tgt, path):
  global soln

  dprint("Src: " + src, 6)
  dprint("Tgt: " + tgt, 6)
  l = len(soln)
  if (l>0):
    if (((l < 100000) and (l % 1000 == 0))):
      dprint("Found " + str(l) + " upgrade paths in %s seconds"  %int(time.time() - start_time))

  if (src == tgt):
    path.append(tgt)
    # dprint ("Path1: " + str(path), 6)
    if not (path in soln):
      soln.append(path)
    dprint("Soln: " + str(soln), 6)
  else:
    for e in lookup[src]:
      p = path[:]
      p.append(src)
      # dprint ("Path: " + str(p), 6)
      createtraversalmatrix(e, tgt, p)

def printTraversalMatrix():
  l = 0
  cnt=0
  while soln:
    p = min(soln, key=lambda x: len(x))
    if (l != (len(p)-1)):
      if (cnt > 1):
        dprint (" ^^ " + str(cnt) + " upgrade paths found", 1)
        cnt=0
      if (len(p) - 1 > hops_desired):
        return
      dprint ("",1)
      dprint ("Upgrade Steps / Hops: " + str(len(p) - 1),1)
      l = len(p) - 1
    cnt+=1
    r = str(p)
#    if (__name__ == '__main__'):
    dprint (" Path: " + r, 0)
    soln.remove(p)
  if (cnt > 1):
    dprint (" ^^ " + str(cnt) + " upgrade paths found",1)
  if (__name__ != '__main__'):
    return r

def main(argv):
  global start_time
  d = dict()
  start_time = time.time()
  d = validateCLIArgsOrFail(argv)
  findAdjacentUpgrades(d['src'], d['tgt'], d['engine'])
  createtraversalmatrix(d['src'], d['tgt'], [])
  r = printTraversalMatrix()
  if (__name__ != '__main__'):
    return r

if __name__ == '__main__':
  main(sys.argv)
