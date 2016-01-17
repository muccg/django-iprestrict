from setuptools import setup

setup(
    name='django-iprestrict',
    version='0.4.0',
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
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django>=1.7',
        'django-templatetag-handlebars==1.3.2.dev1',
    ],
    test_suite='tests.runtests.main',
)
