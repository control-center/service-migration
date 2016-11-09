# service-migration
This repo contains the scripts and Docker container used to perform service migration in Control Center.

## Overview
The service migration is implemented as a python script defined by each service developer.
The script uses the service migration SDK defined in this repo to perform operations
on one or more services.  The script is invoked by serviced, either by the CLI command
`serviced service migrate` or the CLI script directive  `SVC_MIGRATE`.

### Migration SDK
TBD

## Build

The makefile in this repo supports the following targets:

 * `clean` - deletes all intermediate build artifacts (e.g. `.pyc` files)
 * `test` - executes unit-tests for the service migration SDK
 * `wheel - builds the python wheel artifact

The default target will build the wheel in the `dist` subdirectory.

Once you have finished your local testing, commit your changes, push them, and create a pull-request as you would
normally. A Jenkins PR build will be started to verify that your changes will build in
a Jenkins environment.

# Releasing

Use git flow to release a new version to the `master` branch.

The artifact version is defined in the [servicemigration/VERSION](./servicemigration/VERSION) file.

For Zenoss employees, the details on using git-flow to release a version is documented 
on the Zenoss Engineering 
[web site](https://sites.google.com/a/zenoss.com/engineering/home/faq/developer-patterns/using-git-flow).
After the git flow process is complete, a jenkins job can be triggered manually to build and 
publish the artifact. 

