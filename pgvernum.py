import sys

x={}
def dexit(s):
   print (s)
   exit(1)
    
def getPGVersionString(s):
    if (s.count('.')==0):
        a=int(s)
        b=c=0
        if ((a<10) or (a>20)):
            dexit('Invalid PG Version String provided - ' + s)
    elif (s.count('.')==1):
        a,b = map(int,s.split(".", 1))
        if ((a<9) or (b>20)):
            dexit('Invalid PG Version String provided - ' + s)
    elif (s.count('.')==2):
        print ('2')
        a,b,c = map(int, s.split(".", 1))
        if ((b<9) or (b>20)):
            dexit('Invalid PG Version String provided - ' + s)
    else:
        dexit('Invalid PG Version String provided - ' + s)
    
    if (a<10):
        versionnum = a*10000 + (b*100)
    else:
        versionnum = int(a*10000+b)

    print(versionnum)
    

# Currently the default engine is postgres, unless explicitly provided (as 4th Option)
if len(sys.argv) == 2:
    s = sys.argv[1]
else:
    dexit('Invalid number of arguments - ' + str(len(sys.argv)))

getPGVersionString(s)
