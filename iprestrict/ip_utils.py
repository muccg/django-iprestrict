
def get_version(ip):
    return 'ipv4' if '.' in ip else 'ipv6'

def to_number(ip):
    parts= ip.split('.')
    parts = [int(p) for p in reversed(parts)]
    nr = 0
    for i, d in enumerate(parts):
       nr += (256 ** i) * d
    return nr

