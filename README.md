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
Use git flow to release a version to the `master` branch. A jenkins job must be triggered manually to build and publish the
*tar* artifact to zenpip.  During the git flow release process, update the version in the makefile by removing the `dev`
suffix and then increment the version number in the `develop` branch.

## Versioning

The version convention for this artifact is `service-migration-<version>.tar.gz` where `<version>`
is the version of service-migration

By convention, the `develop` branch should have the next revision number, a number higher than what is
currently released, with the `-dev` suffix and the `master` branch will have the currently released version.
For example, if the currently released version is `1.1.0` on master, then
the version in the `develop` should be `1.1.1-dev`.

## Release Steps

1. Check out the `master` branch and make sure to have latest `master`.
  * `git checkout master`
  * `git pull origin master`

2. Check out the `develop` branch.
  * `git checkout develop`
  * `git pull origin develop`

3. Start release of next version. The version is usually the version in the makefile minus the `-dev` suffix.  e.g., if the version
  in `develop` is `1.1.1-dev` and in `master` `1.1.0`, then the
  `<release_name>` will be the new version in `master`, i.e. `0.1.2`.
  *  `git flow release start <release_name>`

4. Update the `VERSION` file. e.g set it to `0.1.2`

5. run `make` to make sure everything builds properly.

6. Commit and tag everything, don't push.
  * `git commit....`
  * `git flow release finish <release_name>`
  * `git push origin --tags`

7. You will be on the `develop` branch again. While on `develop` branch, edit the the `VERSION` file to
be the next development version. For example, if you just released version 0.1.2, then change the `VERSION` file
`1.1.1-dev`.

8. Check in `develop` version bump and push.
  * `git commit...`
  * `git push`

9. Push the `master` branch which should have the new released version.
  * `git checkout master`
  * `git push`

10. Have someone manually kick off the jenkins job to build master which will publish the artifact to zenpip.


