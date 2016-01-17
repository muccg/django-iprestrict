#!/bin/sh

export PYTHONPATH=.
exec django-admin.py test --settings=tests.test_settings tests
