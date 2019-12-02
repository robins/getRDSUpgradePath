# getRDSUpgradePath

![Coverage](https://api.travis-ci.org/robins/getRDSUpgradePath.svg?branch=master)

Python script to find an Upgrade path (from source Version to Target) for any of the AWS RDS Database Engines

## End-user features:
- Compute best (least hops) solution
- Show *all* possible Upgrade paths (if required)
- Show computation progress if taking time
- Support all engines (For e.g. Oracle / SQL Server / MariaDB / Aurora Postgres / etc.)
- Allow (really high) verbosity levels, if required
- Catch trivial errors
  - Source version newer
  - Source Target same
  - Engine name typos / hint correct spelling


## Testing features
- Currently (2019 Dec 1) the project has:
  - Extensive coverage for PG Version Number generation module - 57 tests
    - ^^ with Travis Integration
  - Limited (but working) test coverage for Upgrade path generation


## Releases
- Stable: [Download](https://github.com/robins/getRDSUpgradePath/releases/tag/v1.0)
- Dev: [Download]( https://github.com/robins/getRDSUpgradePath/releases/tag/v1.2 )

## Sample Runs
```

=== Usage / syntax ===
>py getUpgradepath.py

Syntax: python getUpgradePath.py SourceVersion TargetVersion [engine] [hops] [verbosity]

Source / Target Versions are Mandatory. Optionally, you may also provide:
  Engine: RDS Database Engine | Default:postgres
  Hops: Find all upgrade combinations possible within these many Hops | Default:1 | Range:1-10
  Verbosity: Verbosity of the output | Default:1 | Range:1-5

=== Catch trivial errors - (Source Target same) ===
>py getUpgradePath.py 10.6 10.6 postgres
No upgrade required when Source and Target versions are the same

=== Catch trivial errors - (Source version newer) ===
>py getUpgradePath.py 9.3.12 9.3.11 postgres
Cannot upgrade from newer to older version: 9.3.12 -> 9.3.11

=== Catch trivial errors - (Engine name recommendations) ===
>py getUpgradePath.py 9.3.12 9.3.11 auroapostgres
Invalid Engine: auroapostgres
Hint: May be you meant - aurora-postgresql

=== Show 1 Hop (direct upgrade) results by default ===
>py getUpgradePath.py 9.6.15 10.10

Upgrade Steps / Hops: 1
 Path: ['9.6.15', '10.10']

=== Show progress if computation takes longer ===
>py getUpgradePath.py 5.7.16 8.0.16 mysql
Found 1000 upgrade paths in 3 seconds

Upgrade Steps / Hops: 1
 Path: ['5.7.16', '8.0.16']

=== Support all engines - RDS Oracle ===
>py getUpgradePath.py 12.1.0.2.v13 12.1.0.2.v18 oracle-ee

Upgrade Steps / Hops: 1
 Path: ['12.1.0.2.v13', '12.1.0.2.v18']

=== Support all engines - RDS SQL Server ===
>py getUpgradePath.py 12.00.5000.0.v1 14.00.3192.2.v1 sqlserver-ee

Upgrade Steps / Hops: 1
 Path: ['12.00.5000.0.v1', '14.00.3192.2.v1']

=== Support all engines - RDS MariaDB ===
>py getUpgradePath.py 10.0.32 10.3.13 mariadb
Found 1000 upgrade paths in 4 seconds
Found 2000 upgrade paths in 6 seconds
Found 3000 upgrade paths in 9 seconds
Found 4000 upgrade paths in 14 seconds
Found 5000 upgrade paths in 20 seconds

Upgrade Steps / Hops: 1
 Path: ['10.0.32', '10.3.13']

=== Support all engines - Aurora Postgres ===
>py getUpgradePath.py 9.6.3 9.6.12 aurora-postgresql

Upgrade Steps / Hops: 1
 Path: ['9.6.3', '9.6.12']

=== Show *all* possible Upgrade paths ===
>py getUpgradePath.py 9.6.10 10.10 postgres 10

Upgrade Steps / Hops: 1
 Path: ['9.6.10', '10.10']

Upgrade Steps / Hops: 2
 Path: ['9.6.10', '10.9', '10.10']
 Path: ['9.6.10', '10.7', '10.10']
 Path: ['9.6.10', '10.6', '10.10']
 Path: ['9.6.10', '10.5', '10.10']
 Path: ['9.6.10', '9.6.15', '10.10']
 Path: ['9.6.10', '9.6.14', '10.10']
 Path: ['9.6.10', '9.6.12', '10.10']
 Path: ['9.6.10', '9.6.11', '10.10']
 ^^ 9 upgrade paths found

Upgrade Steps / Hops: 3
 Path: ['9.6.10', '10.7', '10.9', '10.10']
 Path: ['9.6.10', '10.6', '10.9', '10.10']
 Path: ['9.6.10', '10.6', '10.7', '10.10']
 Path: ['9.6.10', '10.5', '10.9', '10.10']
 Path: ['9.6.10', '10.5', '10.7', '10.10']
 Path: ['9.6.10', '10.5', '10.6', '10.10']
 Path: ['9.6.10', '9.6.14', '10.9', '10.10']
 Path: ['9.6.10', '9.6.14', '9.6.15', '10.10']
 Path: ['9.6.10', '9.6.12', '10.9', '10.10']
 Path: ['9.6.10', '9.6.12', '10.7', '10.10']
 Path: ['9.6.10', '9.6.12', '9.6.15', '10.10']
 Path: ['9.6.10', '9.6.12', '9.6.14', '10.10']
 Path: ['9.6.10', '9.6.11', '10.9', '10.10']
 Path: ['9.6.10', '9.6.11', '10.7', '10.10']
 Path: ['9.6.10', '9.6.11', '10.6', '10.10']
 Path: ['9.6.10', '9.6.11', '9.6.15', '10.10']
 Path: ['9.6.10', '9.6.11', '9.6.14', '10.10']
 Path: ['9.6.10', '9.6.11', '9.6.12', '10.10']
 ^^ 18 upgrade paths found

Upgrade Steps / Hops: 4
 Path: ['9.6.10', '10.6', '10.7', '10.9', '10.10']
 Path: ['9.6.10', '10.5', '10.7', '10.9', '10.10']
 Path: ['9.6.10', '10.5', '10.6', '10.9', '10.10']
 Path: ['9.6.10', '10.5', '10.6', '10.7', '10.10']
 Path: ['9.6.10', '9.6.12', '10.7', '10.9', '10.10']
 Path: ['9.6.10', '9.6.12', '9.6.14', '10.9', '10.10']
 Path: ['9.6.10', '9.6.12', '9.6.14', '9.6.15', '10.10']
 Path: ['9.6.10', '9.6.11', '10.7', '10.9', '10.10']
 Path: ['9.6.10', '9.6.11', '10.6', '10.9', '10.10']
 Path: ['9.6.10', '9.6.11', '10.6', '10.7', '10.10']
 Path: ['9.6.10', '9.6.11', '9.6.14', '10.9', '10.10']
 Path: ['9.6.10', '9.6.11', '9.6.14', '9.6.15', '10.10']
 Path: ['9.6.10', '9.6.11', '9.6.12', '10.9', '10.10']
 Path: ['9.6.10', '9.6.11', '9.6.12', '10.7', '10.10']
 Path: ['9.6.10', '9.6.11', '9.6.12', '9.6.15', '10.10']
 Path: ['9.6.10', '9.6.11', '9.6.12', '9.6.14', '10.10']
 ^^ 16 upgrade paths found

Upgrade Steps / Hops: 5
 Path: ['9.6.10', '10.5', '10.6', '10.7', '10.9', '10.10']
 Path: ['9.6.10', '9.6.11', '10.6', '10.7', '10.9', '10.10']
 Path: ['9.6.10', '9.6.11', '9.6.12', '10.7', '10.9', '10.10']
 Path: ['9.6.10', '9.6.11', '9.6.12', '9.6.14', '10.9', '10.10']
 Path: ['9.6.10', '9.6.11', '9.6.12', '9.6.14', '9.6.15', '10.10']
 ^^ 5 upgrade paths found

=== Show some level of verbosity ===
>py getUpgradePath.py 9.3.12 9.4.14 postgres 1 2
Calling AWS CLI with 9.3.12 x postgres
Calling AWS CLI with 9.4.14 y postgres
Calling AWS CLI with 9.3.12 9.4.14 postgres
Calling AWS CLI with 9.4.12 9.4.14 postgres
Calling AWS CLI with 9.4.11 9.4.14 postgres
Calling AWS CLI with 9.4.9 9.4.14 postgres
Calling AWS CLI with 9.4.7 9.4.14 postgres
Calling AWS CLI with 9.3.25 9.4.14 postgres
Calling AWS CLI with 9.3.24 9.4.14 postgres
Calling AWS CLI with 9.3.23 9.4.14 postgres
Calling AWS CLI with 9.3.22 9.4.14 postgres
Calling AWS CLI with 9.3.20 9.4.14 postgres
Calling AWS CLI with 9.3.19 9.4.14 postgres
Calling AWS CLI with 9.3.17 9.4.14 postgres
Calling AWS CLI with 9.3.16 9.4.14 postgres
Calling AWS CLI with 9.3.14 9.4.14 postgres

Upgrade Steps / Hops: 1
 Path: ['9.3.12', '9.4.14']

=== High level of verbosity ===
>py getUpgradePath.py 9.4.11 9.4.12 postgres 1 5
Arg array: 9.4.11,9.4.12,postgres,1,5
argv length: 6
Arg 0: getUpgradePath.py
Arg 1: 9.4.11
Arg 2: 9.4.12
Arg 3: postgres
Arg 4: 1
Debug Level: 5
Engine: postgres
Calling AWS CLI with 9.4.11 x postgres
Calling AWS CLI with 9.4.12 y postgres
Source Version: 9.4.11
Target Version: 9.4.12
Cache: Combination not found: 9.4.11->9.4.12
Calling AWS CLI with 9.4.11 9.4.12 postgres
Skip upgrade check from newer to older version: 9.5.19 -> 9.4.12
Skip upgrade check from newer to older version: 9.5.18 -> 9.4.12
Skip upgrade check from newer to older version: 9.5.16 -> 9.4.12
Skip upgrade check from newer to older version: 9.5.15 -> 9.4.12
Skip upgrade check from newer to older version: 9.5.14 -> 9.4.12
Skip upgrade check from newer to older version: 9.5.13 -> 9.4.12
Skip upgrade check from newer to older version: 9.5.12 -> 9.4.12
Skip upgrade check from newer to older version: 9.5.10 -> 9.4.12
Skip upgrade check from newer to older version: 9.5.9 -> 9.4.12
Skip upgrade check from newer to older version: 9.5.7 -> 9.4.12
Skip upgrade check from newer to older version: 9.5.6 -> 9.4.12
Skip upgrade check from newer to older version: 9.4.24 -> 9.4.12
Skip upgrade check from newer to older version: 9.4.23 -> 9.4.12
Skip upgrade check from newer to older version: 9.4.21 -> 9.4.12
Skip upgrade check from newer to older version: 9.4.20 -> 9.4.12
Skip upgrade check from newer to older version: 9.4.19 -> 9.4.12
Skip upgrade check from newer to older version: 9.4.18 -> 9.4.12
Skip upgrade check from newer to older version: 9.4.17 -> 9.4.12
Skip upgrade check from newer to older version: 9.4.15 -> 9.4.12
Skip upgrade check from newer to older version: 9.4.14 -> 9.4.12
Valid targets: 9.4.12
Cache: (9.4.11->{'9.4.12': 1})

Upgrade Steps / Hops: 1
 Path: ['9.4.11', '9.4.12']

```


### Testing Postgres Version Number generation
```
>coverage run test_pgvernum.py
....
----------------------------------------------------------------------
Ran 4 tests in 0.002s

OK
```

### Testing Upgrade Path generation
```
>coverage run test_getUpgradePath.py
.
----------------------------------------------------------------------
Ran 1 test in 2.981s

OK
```
