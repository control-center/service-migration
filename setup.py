import os
from setuptools import setup

root = os.path.abspath(os.path.dirname(__file__))

version = open(os.path.join(root, "servicemigration", "VERSION"), 'r').read().strip()
long_description = open(os.path.join(root, "README.md"), 'r').read()

setup (
    name = "servicemigration",
    version = version,
    description = "Zenoss Control Center Service Migration SDK",
    long_description = long_description,
    url = "https://github.com/control-center/service-migration",
    packages = ["servicemigration"],
    package_data = {
        "servicemigration": ["VERSION"]
    }
)
