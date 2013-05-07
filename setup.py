import re
from setuptools import setup

# Read version from file
VERSION_FILE = 'perm/_version.py'
version_text = open(VERSION_FILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, version_text, re.M)
if mo:
    version = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

# Setup
setup(
    name='django-perm',
    version=version,
    url='https://github.com/dyve/django-perm',
    author='Dylan Verheul',
    author_email='dylan@dyve.net',
    license='Apache License 2.0',
    packages=['perm', 'perm.templatetags'],
    include_package_data=True,
    description='Class based Django permissions for Django models',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Environment :: Web Environment",
        "Framework :: Django",
    ],
)
