# SPDX-FileCopyrightText: Bosch Rexroth AG
#
# SPDX-License-Identifier: MIT
from setuptools import setup

setup(name='testeflask',
      version='2.3.0',
      description='Webserver Sample written in Python for ctrlX',
      author='SDK Team',
      install_requires=['cysystemd','PyJWT', 'ctrlx-datalayer', 'ctrlx-fbs'],
      scripts=['main.py','myproject.py','wsgi.py'],
      packages=['helper'],
      license='MIT License'
      )
