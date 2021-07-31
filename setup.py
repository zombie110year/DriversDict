# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools.command.install import install

class InstallDictionary(install):
    def run(self):
        super().run()
        from driversdict.install import post_install
        post_install()

packages = \
['driversdict']

package_data = \
{'': ['*'], 'driversdict': ['resource/*']}

entry_points = \
{'console_scripts': ['driversdict = driversdict.cli:cli_main']}

cmdclass = {
    "install": InstallDictionary
}

setup_kwargs = {
    'name': 'driversdict',
    'version': '0.1.1',
    'description': '查询、测试、记录「某些压缩包」的解压密码',
    'long_description': None,
    'author': 'zombie110year',
    'author_email': 'zombie110year@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
    'cmdclass': cmdclass,
}


setup(**setup_kwargs)
