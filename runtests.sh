#!/usr/bin/env sh

PYTHONPATH=. coverage run --source=iprestrict django-admin.py test --settings=iprestrict.test_settings iprestrict
