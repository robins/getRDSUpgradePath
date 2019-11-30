# getRDSUpgradePath

![Coverage](https://api.travis-ci.org/robins/getRDSUpgradePath.svg?branch=master)

Python script to find an Upgrade path (from source Version to Target) for any of the AWS RDS Database Engines

## Releases
- Stable: [Download](https://github.com/robins/getRDSUpgradePath/releases/tag/v1.0)
- Dev: [Download]( https://github.com/robins/getRDSUpgradePath/releases/tag/v1.1 )

## Sample Runs
```
>py getUpgradePath.py 9.3.12 10.4 postgres

===============================
Upgrade From: 9.6.9 To: 10.4
Upgrade From: 9.5.13 To: 9.6.9
Upgrade From: 9.4.18 To: 9.5.13
Upgrade From: 9.3.12 To: 9.4.18
===============================

>py getUpgradePath.py 5.5.46 5.7.21 mysql

===============================
Upgrade From: 5.6.39 To: 5.7.21
Upgrade From: 5.5.46 To: 5.6.39
===============================

>py getUpgradePath.py 11.2.0.4.v1 12.1.0.2.v11 oracle-ee

===============================
Upgrade From: 11.2.0.4.v1 To: 12.1.0.2.v11
===============================

>py getUpgradePath.py 10.50.6000.34.v1 14.00.3015.40.v1 sqlserver-ee
Unable to find Upgrade path. Is the Source version supported in RDS?

>py getUpgradePath.py 10.0.17 10.2.12 mariadb

===============================
Upgrade From: 10.1.31 To: 10.2.12
Upgrade From: 10.0.17 To: 10.1.31
===============================

>py getUpgradePath.py 9.6.3 9.6.6 aurora-postgresql

===============================
Upgrade From: 9.6.3 To: 9.6.6
===============================

>py getUpgradePath.py 9.3.12 10.3 postgres

===============================
Unable to find Upgrade path from 9.3.12 to 10.3
===============================

>py getUpgradePath.py 9.3.12
Syntax: python getUpgradePath.py v1 v2 [engine] [1]
Source / Destination Versions are Mandatory. You may also optionally mention Engine (default Postgres) and Debug (1 or 0)

>py getUpgradePath.py 9.3.12 9.4.14 postgres 3
Cache: Combination not found: 9.3.12-x
Calling AWS CLI with 9.3.12 x postgres
Cache: Combination not found: 9.4.14-y
Calling AWS CLI with 9.4.14 y postgres
Cache: Combination not found: 9.3.12-9.4.14
Calling AWS CLI with 9.3.12 9.4.14 postgres
Skip upgrade check from newer to older version: 9.4.24 -> 9.4.14
Skip upgrade check from newer to older version: 9.4.23 -> 9.4.14
Skip upgrade check from newer to older version: 9.4.21 -> 9.4.14
Skip upgrade check from newer to older version: 9.4.20 -> 9.4.14
Skip upgrade check from newer to older version: 9.4.19 -> 9.4.14
Skip upgrade check from newer to older version: 9.4.18 -> 9.4.14
Skip upgrade check from newer to older version: 9.4.17 -> 9.4.14
Skip upgrade check from newer to older version: 9.4.15 -> 9.4.14

===============================
Upgrade From: 9.3.12 To: 9.4.14
===============================


>py getUpgradePath.py 9.3.12 9.4.14 postgres 5
Arg array: 9.3.12,9.4.14,postgres,5
argv length: 5
Arg 0: getUpgradePath.py
Arg 1: 9.3.12
Arg 2: 9.4.14
Arg 3: postgres
Arg 4: 5
Debug Level: 5
Engine: postgres
Cache: Combination not found: 9.3.12-x
Calling AWS CLI with 9.3.12 x postgres
Cache: Combination not found: 9.4.14-y
Calling AWS CLI with 9.4.14 y postgres
Source Version: 9.3.12
Target Version: 9.4.14
Cache: Combination not found: 9.3.12-9.4.14
Calling AWS CLI with 9.3.12 9.4.14 postgres
Skip upgrade check from newer to older version: 9.4.24 -> 9.4.14
Skip upgrade check from newer to older version: 9.4.23 -> 9.4.14
Skip upgrade check from newer to older version: 9.4.21 -> 9.4.14
Skip upgrade check from newer to older version: 9.4.20 -> 9.4.14
Skip upgrade check from newer to older version: 9.4.19 -> 9.4.14
Skip upgrade check from newer to older version: 9.4.18 -> 9.4.14
Skip upgrade check from newer to older version: 9.4.17 -> 9.4.14
Skip upgrade check from newer to older version: 9.4.15 -> 9.4.14
Valid targets: 9.4.14  9.4.12  9.4.11  9.4.9  9.4.7  9.3.25  9.3.24  9.3.23  9.3.22  9.3.20  9.3.19  9.3.17  9.3.16  9.3.14
Cache: (9.3.12-9.4.14->1)  (9.3.12-9.4.12->1)  (9.3.12-9.4.11->1)  (9.3.12-9.4.9->1)  (9.3.12-9.4.7->1)  (9.3.12-9.3.25->1)  (9.3.12-9.3.24->1)  (9.3.12-9.3.23->1)  (9.3.12-9.3.22->1)  (9.3.12-9.3.20->1)  (9.3.12-9.3.19->1)  (9.3.12-9.3.17->1)  (9.3.12-9.3.16->1)  (9.3.12-9.3.14->1)

===============================
Upgrade From: 9.3.12 To: 9.4.14
===============================
```