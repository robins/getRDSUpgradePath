import sys

def dexit(s, shouldexit = 0):
   print (s)
   if (shouldexit):
        exit(1)
    
def getPGVersionString(s):
    dots = s.count('.')
    
    if ( dots> 2):
        dexit('Invalid PG Version String provided - ' + s)
        return -1
    
    x = list(map(int, s.split('.', dots)))
    
    if (x[0]>=10):
        if (dots>=2):
            dexit('Invalid PG Version string provided - ' + s)
            return -1
        versionnum = int(x[0]*10000)
        if (dots ==1):
            versionnum += x[1]
    else:
        if (dots ==0 or dots >2):
            dexit('Invalid PG Version string provided - ' + s)
            return -1
        versionnum = x[0]*10000 + (x[1]*100)
        if (dots ==2):
            versionnum += x[2]
    return versionnum

# Currently the default engine is postgres, unless explicitly provided (as 4th Option)
#if len(sys.argv) == 2:
#    s = sys.argv[1]
#else:
#    dexit('Invalid number of arguments - ' + str(len(sys.argv)))

#print (getPGVersionString(s))