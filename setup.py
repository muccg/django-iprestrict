from setuptools import setup, find_packages

__version__ = '.'.join(map(str, (0, 1, 3)))
__author__ = 'Tamas Szabo'

description = 'Django app + middleware to restrict access to all or sections of a Django project by client IP ranges'

setup(
    name='django-iprestrict',
    version=__version__,
    description=description,
    long_description=description,
    author=__author__,
    url='https://github.com/smalllark/django-iprestrict',
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django>=1.7',
        'django-templatetag-handlebars>=1.2.0',
    ],
    test_suite='tests.runtests.main'
)
