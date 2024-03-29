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
# is possible.

# There are 3 reasons why a source-target combination may not be possible:
# 1. Target Version was released after Source Version
#    1a. For e.g. The upgrade from v9.4.23 -> v9.5.15 is not possible. Here the
#     source version (v9.4.23) was released on 20th Jun 2019 whereas
#     target version (v9.5.15) was released on 8th Nov 2018. Since the source
#     version was release before the target version, this upgrade path is not
#     possible
#    1b. v9.4.12 -> v9.4.1 is not possible for the same reason as Reason 1a above.
# 2. Although Postgres community supports a given version, RDS Postgres doesn't
#    support it yet.
# 3. Although Postgres community supports an upgrade combination, RDS Postgres
#    doesn't support it yet.

import sys
import boto3
import re
import time

from pgvernum import getPGVerNumFromString
from pgvernum import appendMinorVersionIfRequired
from pgvernum import IsVerReleasedAfter
from pgvernum import getVerReleasedDate
from pgvernum import isValidPGVersion
from awsrdscli import isValidRDSEngine
from awsrdscli import getEngineTypoRecommendation
from awsrdscli import getRegionTypoRecommendation

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

      # Don't give Engine Typo recommendations for parameter mix-ups in Command Line
      if (len(d['engine']) > 3):
        dprint("Hint: May be you meant - " + getEngineTypoRecommendation(d['engine']))

      dprint("Common Engines: postgres, mysql, aurora-postgresql, etc.")
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

    if (int(getPGVerNumFromString(d['src'])) == 0):
      dexit('Source Engine Version is invalid: ' + d['src'])
    if (int(getPGVerNumFromString(d['tgt']) == 0)):
      dexit('Target Engine Version is invalid: ' + d['tgt'])
    if ((getPGVerNumFromString(d['src']) >= getPGVerNumFromString(d['tgt']))):
      dexit ('Cannot upgrade from newer to older version: ' + d['src'] + '('  + getVerReleasedDate(d['src']) + ') -> ' + d['tgt'] + '('  + getVerReleasedDate(d['tgt']) + ')')

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
        return -1
  dprint ('Cache: Combination not found: ' + src + '->' + tgt, 3)
  return 0

def callaws(src, tgt, engine):

  dprint('Calling AWS CLI with ' + src + ' ' + tgt + ' ' + engine, 2)
  client = boto3.client('rds')

  # Sample CLI: aws rds describe-db-engine-versions --engine=postgres --engine-version=9.3.12
  resp = client.describe_db_engine_versions(
    Engine=engine,
    EngineVersion=src,
    Filters=[
      {
        'Name': 'status',
        'Values': [
          'deprecated',
          'available'
        ]
      }
    ]
  )

  print (".", end="")
  sys.stdout.flush()

  upgrade_path=resp['DBEngineVersions']
  # Fail if there are no Upgrade paths
  if (not upgrade_path):
    return 0
  else:
    return upgrade_path

def findAdjacentUpgrades(src, tgt, engine, hops_desired):
  global lookup

  dprint("", 3)
  dprint("Find Arg Src: " + src, 6)
  dprint("Find Arg Tgt: " + tgt, 6)
  dprint("Find ArgPath: " + str(hops_desired), 6)

  if (hops_desired < 0):
    dprint('hops < 0. Not diving deeper', 6)
    return
  else:
    dprint ('hops = ' + str(hops_desired), 6)

  if (enable_caching):
    t = cachelookup(src, tgt)
    if (t >= 1):
      return
  else:
    dprint('Caching disabled', 3)

  if (isValidPGVersion(src) and (isValidPGVersion(tgt))):
      if (IsVerReleasedAfter(src, tgt)):
        dprint ('Skip upgrade check for source v' + src + ' (released on ' + getVerReleasedDate(src) + ') after target v' + tgt + ' (released on '+ getVerReleasedDate(tgt) +')', 5)
        return

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
      if (IsVerReleasedAfter(k['EngineVersion'], tgt)):
        dprint ('Skip upgrade check for source v' + k['EngineVersion'] + ' (released on ' + getVerReleasedDate(k['EngineVersion']) + ') after target v' + tgt + ' (released on '+ getVerReleasedDate(tgt) +')', 4)
        continue
      if ((getPGVerNumFromString(k['EngineVersion']) > getPGVerNumFromString(tgt))):
        dprint ('Skip upgrade check from newer to older version: ' + k['EngineVersion'] + ' -> ' + tgt, 4)
        continue

    dprint('Possible Upgrade Target: ' + k['EngineVersion'], 6)

    k2.append(k['EngineVersion'])
    if not (src in lookup):
      lookup[src]={}
    lookup[src][k['EngineVersion']] = 1

  if not k2:
    dprint ('Valid targets: ' + 'NA', 3)
  else:
    dprint ('Valid targets: ' + '  '.join(k2), 4)

  if not lookup:
    dprint ('Cache: NA', 4)
  else:
    dprint ('Cache:', 4)
    dprint ("\n".join('(' + str(e) + '->' + str(lookup[e]) + ')' for e in lookup), 4)

  # Process the list in reversed order since ideally
  # the target is expected to be a recent Minor Version
  for k in (k2):
    # If the next souce-candidate is the target, skip over it
    if not (k == tgt):
      findAdjacentUpgrades(k, tgt, engine, hops_desired - 1)

  # If we reached here, it means this upgrade path isn't possible
  # We mark that and proceed with next possible combination
  if not (src in lookup):
    lookup[src]={}
  if not (tgt in lookup[src]):
    lookup[src][tgt] = 1002
  return

def createtraversalmatrix(src, tgt, path, hops_desired):
  global soln

  dprint("================", 5)
  dprint("Traverse Arg Src: " + src, 5)

  if (hops_desired < 0):
    dprint('hops < 0. Not diving deeper', 7)
    return
  else:
    dprint ('hops = ' + str(hops_desired), 8)

  dprint("Traverse Arg Tgt: " + tgt, 5)
  dprint("Traverse ArgPath: " + str(path), 5)

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
    dprint ('Lookup:', 5)
    dprint ("\n".join('(' + str(e) + '->' + str(lookup[e]) + ')' for e in lookup), 5)
    if src in lookup:
      for e in lookup[src]:
        if (lookup[src][e] == 1):
          dprint ("Src: " + e, 6)
          p = path[:]

          # We intentionally append src and not 'e' since we want the path to start from src
          # for all these iterations
          p.append(src)

          dprint ("Path: " + str(p), 6)
          if (hops_desired >0):
            createtraversalmatrix(e, tgt, p, hops_desired-1)

def printTraversalMatrix():
  global hops_desired
  l = 0
  cnt=0
  printed_something=0

  if not soln:
    r="\nUpgrade path not found. May be you want to increase hop-count and try again."
    dprint(r, 1)
  else:
    while soln:
      p = min(soln, key=lambda x: len(x))
      if (l != (len(p)-1)):
        if (cnt > 1):
          dprint (" ^^ " + str(cnt) + " upgrade paths found", 1)
          cnt=0
        if (len(p) - 1 > hops_desired):
          if not printed_something:
            dprint ('')
            dprint ('There were no Upgrade paths within ' + str(hops_desired) + " hop(s). The simplest upgrade requires at least " + str(len(p) - 1) + ' hops')
            hops_desired = len(p) - 1
          else:
            return
        dprint ("",1)
        dprint ("Upgrade Steps / Hops: " + str(len(p) - 1),1)
        l = len(p) - 1
      cnt+=1
      r = str(p)
      if (__name__ == '__main__'):
        dprint (" Path: " + r, 0)
        printed_something = 1
      soln.remove(p)
    if (cnt > 1):
      dprint (" ^^ " + str(cnt) + " upgrade paths found",1)

  if (__name__ != '__main__'):
    return r

def main(argv):
  global start_time, hops_desired
  d = dict()
  start_time = time.time()
  d = validateCLIArgsOrFail(argv)
  findAdjacentUpgrades(d['src'], d['tgt'], d['engine'], hops_desired)
  createtraversalmatrix(d['src'], d['tgt'], [], hops_desired)
  r = printTraversalMatrix()
  if (__name__ != '__main__'):
    return r

if __name__ == '__main__':
  main(sys.argv)
