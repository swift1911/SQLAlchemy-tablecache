#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os
import platform
import sys
import warnings

try:
    # Use setuptools if available, for install_requires (among other things).
    import setuptools
    from setuptools import setup
except ImportError:
    setuptools = None
    from distutils.core import setup

from distutils.core import Extension
# The following code is copied from
# https://github.com/mongodb/mongo-python-driver/blob/master/setup.py
# to support installing without the extension on platforms where
# no compiler is available.
from distutils.command.build_ext import build_ext


class custom_build_ext(build_ext):
    """Allow C extension building to fail.

    The C extension speeds up websocket masking, but is not essential.
    """

    warning_message = """
********************************************************************
WARNING: %s could not
be compiled. No C extensions are essential for Tornado to run,
although they do result in significant speed improvements for
websockets.
%s

Here are some hints for popular operating systems:

If you are seeing this message on Linux you probably need to
install GCC and/or the Python development package for your
version of Python.

Debian and Ubuntu users should issue the following command:

    $ sudo apt-get install build-essential python-dev

RedHat and CentOS users should issue the following command:

    $ sudo yum install gcc python-devel

Fedora users should issue the following command:

    $ sudo dnf install gcc python-devel

If you are seeing this message on OSX please read the documentation
here:

http://api.mongodb.org/python/current/installation.html#osx
********************************************************************
"""

    def run(self):
        try:
            build_ext.run(self)
        except Exception:
            e = sys.exc_info()[1]
            sys.stdout.write('%s\n' % str(e))
            warnings.warn(self.warning_message % ("Extension modules",
                                                  "There was an issue with "
                                                  "your platform configuration"
                                                  " - see above."))

    def build_extension(self, ext):
        name = ext.name
        try:
            build_ext.build_extension(self, ext)
        except Exception:
            e = sys.exc_info()[1]
            sys.stdout.write('%s\n' % str(e))
            warnings.warn(self.warning_message % ("The %s extension "
                                                  "module" % (name,),
                                                  "The output above "
                                                  "this warning shows how "
                                                  "the compilation "
                                                  "failed."))


kwargs = {}

version = "0.0.1"

if setuptools is not None:
    # If setuptools is not available, you're on your own for dependencies.
    install_requires = []
    install_requires.append('SQLAlchemy')
    if sys.version_info < (2, 7):
        # Only needed indirectly, for singledispatch.
        install_requires.append('ordereddict')
    if sys.version_info < (3, 2):
        install_requires.append('backports.ssl_match_hostname')
    if sys.version_info < (3, 4):
        install_requires.append('singledispatch')
        # Certifi is also optional on 2.7.9+, although making our dependencies
        # conditional on micro version numbers seems like a bad idea
        # until we have more declarative metadata.
        install_requires.append('certifi')
    if sys.version_info < (3, 5):
        install_requires.append('backports_abc>=0.4')
    kwargs['install_requires'] = install_requires

setup(
    name="SQLAlchemy-tablecache",
    version=version,
    packages=["tablecache"],
    author="swift1911",
    author_email="swift1911@163.com",
    url="http://github.com/swift1911",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    description="sqlAlchemy-tablecache is a table cache tools for sqlAlchemy",
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    **kwargs
)
