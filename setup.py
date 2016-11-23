import os
import re
from setuptools import setup

def get_package_version(package):
    version = re.compile(r"(?:__)?version(?:__)?\s*=\s\"(.*)\"", re.I)
    initfile = os.path.join(os.path.dirname(__file__), package, "__init__.py")
    for line in open(initfile):
        m = version.match(line)
        if m:
            return m.group(1)
    return "UNKNOWN"

setup(
    name='django-iprestrict',
    version=get_package_version("iprestrict"),
    description='Django app + middleware to restrict access to all or sections of a Django project by client IP ranges',
    long_description='Django app + middleware to restrict access to all or sections of a Django project by client IP ranges',
    author='Tamas Szabo, CCG, Murdoch University',
    author_email='devops@ccg.murdoch.edu.au',
    url='https://github.com/muccg/django-iprestrict',
    download_url='https://github.com/muccg/django-iprestrict/releases',
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
    packages=[
        'iprestrict',
        'iprestrict.management',
        'iprestrict.management.commands',
        'iprestrict.migrations',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django>=1.8',
        'django-templatetag-handlebars==1.3.1',
    ],
    extras_require={
        'geoip': [
            'pycountry==1.20',
            'geoip2==2.4.0',
            'GeoIP==1.3.2',
            ],
        'dev': [
            'tox',
            'pep8',
            'flake8',
            'mock',
            'Sphinx',
            'django-extensions',
            'Werkzeug',
            ],
    },
    test_suite='tests.runtests.main',
)
