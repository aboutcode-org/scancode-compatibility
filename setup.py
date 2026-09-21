#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# SPDX-FileCopyrightText: 2026 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import
from __future__ import print_function

from glob import glob
from os.path import basename
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


desc = '''A ScanCode post-scan plugin to to illustrate the creation of a simple post-scan plugin.'''

setup(
    name='scancode-compatibility',
    version='1.0.0',
    license='',
    description=desc,
    long_description=desc,
    author='Henrik Sandklef',
    author_email='hesa@software-compliance.org',
    license_files=('LICENSES/GPL-3.0-or-later.txt',),
    url='https://codeberg.org/software-compliance-org/scancode-compatibility',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
    keywords=[
        'scancode', 'plugin', 'post-scan'
    ],
    install_requires=[
        'scancode-toolkit',
    ],
    entry_points={
        'scancode_post_scan': [
            'compatibility = compatibility_scancode.compatibility_scancode:Compatibility',
        ],
    }
)
