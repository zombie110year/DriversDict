# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools.command.install import install
from pathlib import Path

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
    'version': '0.2.0',
    'description': '查询、测试、记录「某些压缩包」的解压密码',
    'long_description': Path("README.md").read_text("utf-8"),
    'long_description_content_type': 'text/markdown',
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
