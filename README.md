# getRDSUpgradePath
Python script to find all possible Upgrade paths (from one Version to another) for AWS RDS Database Engines

Sample Runs
```
C:\proj\aws_rds_postgres_upgrade_path>python getUpgradePath.py 9.3.12 9.6.6
From: 9.5.10 To:9.6.6
From: 9.4.15 To:9.5.10
From: 9.3.12 To:9.4.15

C:\proj\aws_rds_postgres_upgrade_path>python getUpgradePath.py 9.3.12
Syntax: python getUpgradePath.py v1 v2 [engine]
Source / Destination Versions are Mandatory. You may also optionally mention Engine (default Postgres)
```