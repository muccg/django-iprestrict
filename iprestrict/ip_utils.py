# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def get_version(ip):
    return 'ipv4' if '.' in ip else 'ipv6'


def to_number(ip):
    parts = ip.split('.')
    parts = [int(p) for p in reversed(parts)]
    nr = 0
    for i, d in enumerate(parts):
        nr += (256 ** i) * d
    return nr


def to_ip(number):
    mask = int('1' * 8, 2)
    parts = []
    for i in range(4):
        shifted_number = number >> (8 * i)
        parts.append(shifted_number & mask)

    return '.'.join(map(lambda i: str(i), reversed(parts)))


def cidr_to_range(ip, prefix_length):
    ip = to_number(ip)
    start_mask = int('1' * prefix_length, 2) << (32 - prefix_length)
    end_mask = int('1' * (32 - prefix_length), 2)
    start = ip & start_mask
    end = start | end_mask
    return (start, end)
