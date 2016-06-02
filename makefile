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
VENV_ACTIVATE_CMD := . $(PROJECT_DIR)/venv/bin/activate


default: wheel

clean:
	rm -f servicemigration/*.pyc
	rm -f tests/*.pyc
	rm -rf build
	rm -rf dist
	rm -rf $(PROJECT_DIR)/venv

test:
	python -m unittest discover

wheel: venv
	$(VENV_ACTIVATE_CMD); \
	python setup.py bdist_wheel

example:
	MIGRATE_INPUTFILE=tests/v1.0.0.json MIGRATE_OUTPUTFILE=out.json python example.py

run-example:
	serviced service migrate Zenoss.core example.py

venv:
	virtualenv $(PROJECT_DIR)/venv
	$(VENV_ACTIVATE_CMD); \
	pip install -r $(PROJECT_DIR)/requirements.txt
