# This script allows working with Postgres Version Numbers and tries
# to provide basic modules around it. It provides functions to:
# 1) Conversion - For e.g. getPGVerNumFromString() is a function that
#    converts any Postgres version string (for e.g. v9.3.14) to
#    corresponding version Number - i.e. 90314
# 2) Validity - For e.g. IsValidPGVersion() allows validity checks

# Note: It also takes care of the new Version numbering system in effect
# since Postgres v10+

# Sample runs
# -----------
# >py pgvernum.py 9.3.14
# 90314
# >py pgvernum.py 9.6.1
# 90601
# >py pgvernum.py 10.0
# 100000
# >py pgvernum.py 10.14
# 100014
# >py pgvernum.py 11.1
# 110001


import sys
import re
from datetime import datetime

debug_level = 0
default_debug_level = 1

verReleaseDates = {
  '120001': 20191114
}

def dprint(s, debug = default_debug_level):
  if (debug_level >= debug):
    print (s)

def isValidPGVersion(_s, debug = default_debug_level):

  s= str(_s)
  # Old (v9.3.1) or New (v11.0) require at least 4 characters for
  # being a valid version string
  if (len(s)<4):
    dprint('Invalid Version String - Requires at least 4 characters - ' + s, debug)
    return 0

  if (re.match(r"^\.|.*\.$", s)):
    dprint("Invalid Version String. Shouldn't begin or end with period / dot (.) - " + s, debug)
    return 0

  # Fail if there are 2 or more adjacent dots (.)
  if (re.match(r".*[\.]{2,}", s)):
    dprint("Invalid Version String. There are 2+ adjacent periods / dots (.) - " + s, debug)
    return 0

  dots = s.count('.')

  # Fail if it has anything except numbers and dot (.)
  if (not re.match(r'^[0-9\.]*$', s)):
    dprint("Invalid Version String. Shouldn't have anything except numbers and period / dot (.) - " + s, debug)
    return 0

  # Fail if it has no dots. A Version requires both Major AND Minor
  # version to be present.
  #
  # There are other functions that act as fallback, that can convert
  # some Major Version strings to a valid Postgres Versions by appending
  # a ".0" minor version, but that is beyond scope of this function
  if (dots == 0):
    dprint("Invalid Version String. Should have both Major and Minor version - " + s, debug)
    return 0

  # Fail if it has more than 2 dots
  if (dots > 2):
    dprint("Invalid Version String. Has more than 2 periods / dots (.) - " + s, debug)
    return 0

  x = list(map(int, s.split('.', dots)))

  if (dots == 2):
    # v10+ should not have more than 1 dot
    if (x[0]>=10):
      dprint("Invalid Version String. v10+ shouldn't have more than one period / dot (.) - " + s, debug)
      return 0
    if (x[2] >= 100):
      dprint("Invalid Version String. Minor version should be less than 100 - " + s, debug)
      return 0
    if (x[1] >= 100):
      dprint("Invalid Version String. Right digit of Major version (9.x) should be <100 - " + s, debug)
      return 0

  if (dots == 1):
    # pre-v10 should have more than 1 dot
    if (x[0]<10):
      dprint("Invalid Version String. Should have both Major and Minor versions - " + s, debug)
      return 0
    if (x[1] >= 10000):
      dprint("Invalid Version String. Minor Version should be less than 10000 - " + s, debug)
      return 0

  return 1

def getMajorPGVersion(s):
  if (not isValidPGVersion(s)):
    return -1

  dots = s.count('.')
  x = list(map(int, s.split('.', dots)))

  # This is pre-v10
  if (dots == 2):
    return float(str(x[0]) + "." + str(x[1]))
  # This is v10+
  elif (dots == 1):
    return float(x[0])

  # We shouldn't reach here. Something went wrong
  return -2

def getMinorPGVersion(s):
  if (not isValidPGVersion(s)):
    return -1

  dots = s.count('.')
  x = list(map(int, s.split('.', dots)))

  # This is pre-v10
  if (dots == 2):
    return x[2]
  # This is v10+
  elif (dots == 1):
    return x[1]

  # We shouldn't reach here. Something went wrong
  return -2

# Returns a dict of [Major, Minor] if provided a valid PG Version
def parsePGVersion(s):

  if (not isValidPGVersion(s)):
    return -1

  Maj = getMajorPGVersion(s)
  Min = getMinorPGVersion(s)

  if (Maj >= 0):
    if (Min >= 0):
      return [Maj, Min]

  return -1

def appendMinorVersionIfRequired(s):

  if (not isValidPGVersion(s)):
    attempt1 = s + ".0"
    if (isValidPGVersion(attempt1)):
      return attempt1

  return s

def getPGVerNumFromString(s):

  if (not isValidPGVersion(s)):
    return 0

  dots = s.count('.')

  x = list(map(int, s.split('.', dots)))

  if (x[0]>=10):
    versionnum = int(x[0]*10000)
    if (dots == 1):
      versionnum += x[1]
  else:
    versionnum = x[0]*10000 + (x[1]*100)
    if (dots ==2):
      versionnum += x[2]
  return versionnum

def getVerReleasedDate(v):
  global verReleaseDates

  ver=str(getPGVerNumFromString(v))
  if isValidPGVersion(ver):
    return '0'

  if (ver in verReleaseDates):
    return datetime.strptime(str(verReleaseDates[ver]), '%Y%m%d').strftime('%Y-%m-%d')
  else:
    dprint('Release date unavailable for release: ' + ver)
  return '0'

def isVerReleasedAfter(v, dt):
  global verReleaseDates

  ver=str(getPGVerNumFromString(v))

# XXX: Currently assuming that v is a valid version NUMBER (not string)
#  if not isValidPGVersion(ver):
#    return 0

  if (ver in verReleaseDates):
    t=int(datetime.strptime(str(dt), '%Y-%m-%d').strftime('%Y%m%d'))

    if verReleaseDates[ver]>t:
      return 1
  else:
    dprint('Release date unavailable for release: ' + v)

  return 0

def main(argv):
  if len(sys.argv) == 2:
    s = sys.argv[1]
  else:
    dprint('Invalid number of arguments - ' + str(len(sys.argv)), 0)
    exit()
  print (getVerReleasedDate(s))

  if (__name__ != '__main__'):
    return r

if (__name__ == '__main__'):
  main(sys.argv)