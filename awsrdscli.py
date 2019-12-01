import sys

from textdistance import levenshtein

list = ['aurora-mysql', 'aurora-postgresql', 'aurora', 'docdb', 'mariadb', 'mysql', 'neptune', 'oracle-ee', 'postgres', 'sqlserver-ee', 'sqlserver-ex', 'sqlserver-se', 'sqlserver-web']

def isValidRDSEngine(s):

  if s in list:
    return 1
  else:
    return 0

# Ideally we should be checking for distance only when there is a spelling error
# (a.k.a. s not in list), but for an ad-hoc solution this doesn't hurt for now
def getEngineTypoRecommendation(s):
  recommendation = min(list, key = lambda x: levenshtein(s, x))
  return recommendation

# C:\Users\tharar>aws rds describe-db-engine-versions | grep "\"Engine\"" | sed "s/^ *//;s/ *$//" | sort | uniq
# "Engine": "aurora-mysql",
# "Engine": "aurora-postgresql",
# "Engine": "aurora",
# "Engine": "docdb",
# "Engine": "mariadb",
# "Engine": "mysql",
# "Engine": "neptune",
# "Engine": "oracle-ee",
# "Engine": "postgres",
# "Engine": "sqlserver-ee",
# "Engine": "sqlserver-ex",
# "Engine": "sqlserver-se",
# "Engine": "sqlserver-web",