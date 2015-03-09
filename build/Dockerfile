# This file defines the standard Docker image used to execute service
# migrations for upgrading servcies in Control Center.
#
FROM python:2.7.9

MAINTAINER Zenoss, Inc <dev@zenoss.com>

RUN mkdir -p /usr/share/serviced/migration
COPY servicemigration /usr/share/serviced/migration/servicemigration
ENV PYTHONPATH /usr/share/serviced/migration

#
# This is the directory that will be the mount point for the service migration files.
#
WORKDIR /migration
