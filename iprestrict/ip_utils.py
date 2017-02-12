# -*- coding: utf-8 -*-
from __future__ import unicode_literals


IPv4 = 'ipv4'
IPv6 = 'ipv6'


def get_version(ip):
    return IPv6 if ':' in ip else IPv4


def is_ipv4(ip):
    return get_version(ip) == IPv4


def is_ipv6(ip):
    return get_version(ip) == IPv6


def to_number(ip):
    return ipv6_to_number(ip) if is_ipv6(ip) else ipv4_to_number(ip)


def ipv4_to_number(ip):
    return _ip_to_number(ip)


def ipv6_to_number(ip):
    if '.' in ip:
        ip = convert_mixed(ip)
    if '::' in ip:
        ip = explode(ip)
    return _ip_to_number(ip, separator=':', group_size=2 ** 16, base=16)


def explode(ip):
    if ip.count('::') > 1:
        raise ValueError('Invalid ip address "%s". "::" can appear only once.' % ip)
    pre, post = [reject_empty(x.split(':')) for x in ip.split('::')]
    return ':'.join(pre + ['0'] * (8 - len(pre) - len(post)) + post)


def convert_mixed(ip):
    last_colon = ip.rfind(':')
    ipv6, ipv4 = ip[:last_colon+1], ip[last_colon+1:]
    if ipv4.count('.') != 3:
        raise ValueError('Invalid IPv6 address "%s". Dotted ipv4 part should be at the end.' % ip)
    a, b, c, d = ipv4.split('.')
    pre_last = 256 * int(a) + int(b)
    last = 256 * int(c) + int(d)

    return '%s:%x:%x' % (ipv6, pre_last, last)


def to_ip(number, version=IPv4):
    if version == IPv6:
        separator = ':'
        parts_count = 8
        parts_length = 16
        fmt = '%x'
    else:
        separator = '.'
        parts_count = 4
        parts_length = 8
        fmt = '%d'
    mask = int('1' * parts_length, 2)
    parts = []
    for i in range(parts_count):
        shifted_number = number >> (parts_length * i)
        parts.append(shifted_number & mask)

    return separator.join(map(lambda i: fmt % i, reversed(parts)))


def cidr_to_range(ip, prefix_length):
    ip_length = 128 if is_ipv6(ip) else 32
    ip = to_number(ip)
    start_mask = int('1' * prefix_length, 2) << (ip_length - prefix_length)
    end_mask = int('1' * (ip_length - prefix_length), 2)
    start = ip & start_mask
    end = start | end_mask
    return (start, end)


def _ip_to_number(ip, separator='.', group_size=2 ** 8, base=10):
    parts = ip.split(separator)
    parts = [int(p, base) for p in reversed(parts)]
    nr = 0
    for i, d in enumerate(parts):
        nr += (group_size ** i) * d
    return nr


def reject_empty(l):
    return [x for x in l if x]
