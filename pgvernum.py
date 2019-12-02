# This script allows importing getPGVersionString() function that converts
# any Postgres version string (for e.g. v9.3.14) to corresponding
# Postgres version Number, i.e. 90314.

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

debug_level = 0
default_debug_level = 1

def dprint(s, debug = default_debug_level):
  if (debug_level >= debug):
    print (s)

def isValidPGVersion(s, debug = default_debug_level):

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

  # v10+ should not have more than 1 dot
  if (dots == 2):
    if (x[0]>=10):
      dprint("Invalid Version String. v10+ shouldn't have more than one period / dot (.) - " + s, debug)
      return 0

  # pre-v10 should have more than 1 dot
  if (dots == 1):
    if (x[0]<10):
      dprint("Invalid Version String. Should have both Major and Minor versions - " + s, debug)
      return 0

  return 1


def getMajorVersion(s):
  return

def getMinorVersion(s):
  return

def parsePGVersion(s):

  if (not isValidPGVersion(s)):
    return -1





def appendMinorVersionIfRequired(s):
  if(s.count('.') == 0):
    return s + ".0"
  else:
    return s

def getPGVersionString(s):

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

#if len(sys.argv) == 2:
#  s = sys.argv[1]
#else:
#  dexit('Invalid number of arguments - ' + str(len(sys.argv)))

#print (getPGVersionString(s))