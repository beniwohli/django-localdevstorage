import sys

from setuptools import setup, find_packages
from localdevstorage import __version__ as version

from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name = 'django-localdevstorage',
    version = version,
    description = 'A Django storage backend for local development that downloads files from the live site on the fly.',
    author = 'Benjamin Wohlwend',
    author_email = 'piquadrat@gmail.com',
    url = 'https://github.com/piquadrat/django-localdevstorage',
    packages = find_packages(),
    zip_safe=False,
    include_package_data = True,
    install_requires=[
        'Django>=1.2',
        'requests>=1.0',
    ],
    tests_require=['pytest', 'pytest-django', 'responses'],
    cmdclass={'test': PyTest},
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ]
)
