from setuptools import setup, find_packages
from localdevstorage import __version__ as version

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
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ]
)
