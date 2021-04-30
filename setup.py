import os
import re

from setuptools import find_packages, setup

ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([a-zA-Z0-9.]+)['"]''')


def get_version():
    init = open(os.path.join(ROOT, 'teflo_terraform_plugin', '__init__.py')).read()
    return VERSION_RE.search(init).group(1)


setup(
    name='teflo_terraform_plugin',
    version=get_version(),
    description="teflo provisioner plugin",
    author="Red Hat Inc",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "teflo"
    ],
    entry_points={

            'provisioner_plugins': 'teflo_terraform_plugin = teflo_terraform_plugin:TerraformProvisionerPlugin',

    }
)
os.system('source scripts/install_terraform.sh')