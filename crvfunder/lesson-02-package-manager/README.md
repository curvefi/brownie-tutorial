# CRVFunder 2: Package Manager

## [🎥 Video 2: Package Manager 🎬](https://youtu.be/yAB25Cn8o8c)

The CRVFunder series is a short series exploring using Brownie at an application level.  Specifically, we'll be looking at how Brownie was used to help rapidly prototype the CRVFunder application.  CRVFunder launched a new fundraising gauge type to divert CRV inflation to any cause as voted on by the Curve DAO.

Throughout this series we'll be pointing to snapshots of the code in development.  The actual repository is available at [@vefunder/crvfunder](https://github.com/vefunder/crvfunder/).  The code contained here in the crvfunder directory shows the application snapshot as it existed at [74d51bc](https://github.com/vefunder/crvfunder/commit/74d51bc52bcae05c6d77d3a240b883b315526de9)


## PYTEST EXIT CODES
Running pytest will return one of the following exit codes

0. OK
1. TESTS_FAILED
2. INTERRUPTED
3. INTERNAL_ERROR
4. USAGE_ERROR
5. NO_TESTS_COLLECTED


## FIXTURE SCOPE
The scope of the fixture can be passed to determine when the fixture is destroyed

- **function:** (default) fixture destroyed at end of test
- **class:** fixture destroyed at last test in class
- **module:** fixture destroyed at last test in module
- **session:** fixture destroyed at end of test session


## BROWNIE PACKAGE MANAGER
Brownie allows you to install external packages and projects from Github.

**From the Command Line**

    brownie pm install [ORGANIZATION]/[REPOSITORY]@[VERSION]

**Python Fixture**

    pm("[ORGANIZATION]/[REPOSITORY]@[VERSION]")


