# Copyright 2015 The Serviced Authors.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

PROJECT_DIR      := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

# Define the image name, version and tag name for the docker build image
BUILD_IMAGE = build-tools
BUILD_VERSION = 0.0.5
TAG = zenoss/$(BUILD_IMAGE):$(BUILD_VERSION)

UID := $(shell id -u)
GID := $(shell id -g)

DOCKER_RUN := docker run --rm \
                -v $(PWD):/mnt \
                --user $(UID):$(GID) \
                $(TAG) \
                /bin/bash -c

default: wheel

clean:
	rm -f *.whl
	rm -f servicemigration/*.pyc
	rm -f tests/*.pyc
	rm -rf build
	rm -rf dist
	rm -rf $(PROJECT_DIR)/venv

test:
	$(DOCKER_RUN) "cd /mnt && python -m unittest discover"

wheel:
	@echo "Building a binary distribution of service-migration"
	$(DOCKER_RUN) "cd /mnt && python setup.py bdist_wheel"

example:
	MIGRATE_INPUTFILE=tests/v1.0.0.json MIGRATE_OUTPUTFILE=out.json python example.py

run-example:
	serviced service migrate Zenoss.core example.py
