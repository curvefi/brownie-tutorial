# CRVFunder 1: pre-commit

## [🎥 Video 1: Pre-Commit 🎬](https://youtu.be/yfTCF0yVW6k)

The CRVFunder series is a short series exploring using Brownie at an application level.  Specifically, we'll be looking at how Brownie was used to help rapidly prototype the CRVFunder application.  CRVFunder launched a new fundraising gauge type to divert CRV inflation to any cause as voted on by the Curve DAO.

Throughout this series we'll be pointing to snapshots of the code in development.  The actual repository is available at [@vefunder/crvfunder](https://github.com/vefunder/crvfunder/).  The code contained here in the crvfunder directory shows the application snapshot as it existed at [74d51bc](https://github.com/vefunder/crvfunder/commit/74d51bc52bcae05c6d77d3a240b883b315526de9)


## GIT HOOKS
Git Hooks are a way to fire off custom scripts when certain important actions occur.  Pre-commit inspects a snapshot before it is committed.  Further details at: [https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)


## GITHUB ACTIONS MIX
A Brownie template preconfigured for continuous integration with Github Actions, standardized testing environments with tox, linting checks (black, flake8, isort) and pre-commit for linting hooks. To create an empty brownie environment configured with github actions

> brownie bake github-actions

Additional Brownie mixes can be browsed in the [@brownie-mix](https://github.com/brownie-mix/) Github repository.


## LINTING TOOLS
Linters are tools used to flag programming errors, bugs, and coding issues

 * [black](https://black.readthedocs.io): a PEP 8 compliant opinionated formatter with its own style 
 * [flake8](flake8.pycqa.org): wrapper for PyFlakes, pycodestyle + McCabe 
 * [isort](pycqa.github.io/isort): Python utility to organize imports 


## PRECOMMIT CONFIG
Configuration details for linters are stored in [.precommit-config.yaml](https://github.com/zcor/brownie-tutorial/blob/main/crvfunder/lesson-01-precommit/crvfunder/.pre-commit-config.yaml)

