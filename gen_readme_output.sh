# Syntactic checks
py getUpgradepath.py
py getUpgradePath.py 10.6 10.6 postgres

# Validation checks
py getUpgradePath.py 9.6.15 10.10
py getUpgradePath.py 9.6.3 9.6.12 aurora-postgresql
py getUpgradePath.py 5.5.46 5.7.21 mysql
py getUpgradePath.py 11.2.0.4.v1 12.1.0.2.v11 oracle-ee
py getUpgradePath.py 10.50.6000.34.v1 14.00.3015.40.v1 sqlserver-ee
py getUpgradePath.py 10.0.17 10.2.12 mariadb
py getUpgradePath.py 9.6.3 9.6.12 aurora-postgresql
py getUpgradePath.py 9.3.12 10.4 postgres

# Negative Test Cases
py getUpgradePath.py 9.3.12
py getUpgradePath.py 9.3.12 9.4.14 postgres 5
#py getUpgradePath.py 10.5 10.6d postgres