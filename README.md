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

The default target will build the wheel.
