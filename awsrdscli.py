import sys

def isValidRDSEngine(s):
    list = ['aurora-mysql', 'aurora-postgresql', 'aurora', 'docdb', 'mariadb', 'mysql', 'neptune', 'oracle-ee', 'postgres', 'sqlserver-ee', 'sqlserver-ex', 'sqlserver-se', 'sqlserver-web']

    if s not in list:
        return 0

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