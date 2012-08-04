#!/usr/bin/env sh

PYTHONPATH=. django-admin.py test --settings=iprestrict.test_settings iprestrict
