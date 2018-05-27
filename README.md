# getRDSUpgradePath
Python script to find all possible Upgrade paths (from one Version to another) for AWS RDS Database Engines

Sample Runs
```
>python getUpgradePath.py 9.3.12 9.6.6
From: 9.5.10 To:9.6.6
From: 9.4.15 To:9.5.10
From: 9.3.12 To:9.4.15

>python getUpgradePath.py 9.3.12 10.3 postgres
Upgrade From: 9.6.8 To: 10.3
Upgrade From: 9.5.12 To: 9.6.8
Upgrade From: 9.4.17 To: 9.5.12
Upgrade From: 9.3.12 To: 9.4.17

>python getUpgradePath.py 5.5.46 5.7.21 mysql
Upgrade From: 5.6.39 To: 5.7.21
Upgrade From: 5.5.46 To: 5.6.39

>python getUpgradePath.py 11.2.0.4.v1 12.1.0.2.v11 oracle-ee
Upgrade From: 11.2.0.4.v1 To: 12.1.0.2.v11

>python getUpgradePath.py 10.50.6000.34.v1 14.00.3015.40.v1 sqlserver-ee
Upgrade From: 13.00.4466.4.v1 To: 14.00.3015.40.v1
Upgrade From: 10.50.6000.34.v1 To: 13.00.4466.4.v1

>python getUpgradePath.py 10.0.17 10.2.12 mariadb
Upgrade From: 10.1.31 To: 10.2.12
Upgrade From: 10.0.17 To: 10.1.31

>python getUpgradePath.py 9.6.3 9.6.6 aurora-postgresql
Upgrade From: 9.6.3 To: 9.6.6

>python getUpgradePath.py 9.6.3 9.6.4
Unable to find Upgrade path

>python getUpgradePath.py 9.3.12
Syntax: python getUpgradePath.py v1 v2 [engine]
Source / Destination Versions are Mandatory. You may also optionally mention Engine (default Postgres)
```