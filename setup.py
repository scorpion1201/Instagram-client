#!/usr/bin/env python

import io
import os
import sys
import textwrap
import setuptools

here = os.path.dirname(__file__)

setup_params = dict(
    name="Instagram",
    version="0.1.1",
    description="Instagram-client API",
    author="scorpion1201",
    author_email="me@5corpion.dev",
    license="MIT",
    keywords="Instagram crawl",
    url="https://github.com/scorpion1201/Instagram-client",
    src_root=None,
    packages=setuptools.find_packages("."),
    include_package_data=True,
    zip_safe=False,
    classifiers=textwrap.dedent("""
        Development Status :: 4 - Beta
        Intended Audience :: Developers
        License :: OSI Approved :: MIT License
        Operating System :: OS Independent
        Programming Language :: Python :: 3.5
        Programming Language :: Python :: 3.6
        Topic :: Internet
        Topic :: Software Development :: Libraries
        Topic :: Software Development :: Libraries :: Python Modules
        Topic :: Utilities
        """).strip().splitlines(),
    python_requires='!=2.*.*,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
    setup_requires=['requests'],
)

if __name__ == "__main__":
    here and os.chdir(here)
    dist = setuptools.setup(**setup_params)

