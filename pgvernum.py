# This script allows importing getPGVersionString() function that converts
# any Postgres version string (for e.g. v9.3.14) to corresponding
# Postgres version Number, i.e. 90314.

# Note: It takes care of the Version numbering change since Postgres v10

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

debug_level = 2
default_debug_level = 1

def dprint(s, debug = default_debug_level):
   if (debug_level >= debug):
      print (s)

def getPGVersionString(s):
    dots = s.count('.')

    if ( dots> 2):
        dprint('Invalid Postgres version String provided - ' + s, 1)
        return -1

    x = list(map(int, s.split('.', dots)))

    if (x[0]>=10):
        if (dots>=2):
            dprint('Invalid Postgres version string provided - ' + s, 1)
            return -1
        versionnum = int(x[0]*10000)
        if (dots ==1):
            versionnum += x[1]
    else:
        if (dots ==0 or dots >2):
            dprint('Invalid Postgres version string provided - ' + s, 1)
            return -1
        versionnum = x[0]*10000 + (x[1]*100)
        if (dots ==2):
            versionnum += x[2]
    return versionnum

#if len(sys.argv) == 2:
#    s = sys.argv[1]
#else:
#    dexit('Invalid number of arguments - ' + str(len(sys.argv)))

#print (getPGVersionString(s))