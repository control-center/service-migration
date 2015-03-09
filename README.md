# service-migration
This repo contains the scripts and Docker container used to perform service migration in Control Center.

## Overview
The service migration is implemented as a python script defined by each service developer.
The script uses the service migration SDK defined in this repo to perform operations
on one or more services.  The script is invoked by serviced, either by the CLI command
`serviced service migrate` or the CLI script directive  `SVC_MIGRATE`.

### Migration SDK
TBD

## Docker Container

serviced runs the script in a Docker container using the Docker image defined by this repo.
The image expects the migration script and its input/ouput files to be be mounted into the `/migration`
directory within the image.  The SDK expects the caller to pass two files as arguments to the Python script:
 * a JSON file containing an array of 1 or more service definitions
 * the output file which will contain the modified JSON array if the migration completes successfully

The caller can invoke the migration script with a command like:
```
docker run --rm -t -v "$PWD"/migration:/migration zenoss/service-migration:v1 python /migration/migrate.py /migration/input.json /migration/output.json;
```

## Build

The makefile in this repo supports the following targets:

 * `clean` - deletes all intermediate build artifacts (e.g. `.pyc` files)
 * `test` - executes unit-tests for the service migration SDK
 * `buildImage` - builds the Docker image containing the migration SDK

The default target will execute the unit-tests and build the docker image.
