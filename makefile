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

IMAGE_NAME      := zenoss/service-migration
IMAGE_TAG       := $(shell cat servicemigration/VERSION)
IMAGE_VERSION   := $(shell python -c "print '.'.join('$(IMAGE_TAG)'.split('.')[0])")

default: buildImage

clean:
	rm -f servicemigration/*.pyc
	rm -f tests/*.pyc
	rm -rf build/servicemigration

buildImage: copySource
	docker build -t $(IMAGE_NAME)_v$(IMAGE_VERSION):$(IMAGE_TAG) build

copySource: test clean
	cp -r servicemigration build/servicemigration

test:
	python -m unittest discover

pushImage:
	docker push $(IMAGE_NAME)_v$(IMAGE_VERSION):$(IMAGE_TAG)

wheel:
	python setup.py bdist_wheel
	mv dist/* .
	rm -rf build/bdist.linux-x86_64 build/lib.linux-x86_64-2.7 servicemigration.egg-info dist
