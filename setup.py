#!/usr/bin/env python

from setuptools import setup

setup(
    name='django-iprestrict',
    version='0.3.2',
    description='Django app + middleware to restrict access to all or sections of a Django project by client IP ranges',
    long_description='Django app + middleware to restrict access to all or sections of a Django project by client IP ranges',
    author='Tamas Szabo, CCG, Murdoch University',
    author_email='devops@ccg.murdoch.edu.au',
    url='https://github.com/muccg/django-iprestrict',
    download_url='https://github.com/muccg/django-iprestrict/releases',
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
    packages=[
        'iprestrict',
        'iprestrict.management',
        'iprestrict.management.commands',
    ],
    include_package_data=True,
    install_requires=[
        'South>=1.0.0',
        'django-templatetag-handlebars==1.2.0',
    ]
)
