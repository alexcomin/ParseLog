__author__ = 'aleksandr.komin'

from time import sleep
import re
from datetime import datetime


def fill_dict(m_dictionary, m_key, in_value):
    m_dictionary[m_key] = list(map(sum, zip(m_dictionary.get(m_key, [0, 0]),
                                            [1, in_value])))


def clean(domain):
    if domain.startswith('www.'):
        domain = domain.replace('www.', '', 1)
    if domain.endswith(':80'):
        domain = domain.rsplit(':', 1)[0]
    return domain


def get_prn(m_list, m_dictionary):
    for key in m_list:
        a, b = m_dictionary.get(key, (0, 0))
        write_file('s1.txt', out_fmt.format(key, a, b, b / a if a else 0))
        # print(out_fmt.format(key, a, b, b / a if a else 0))


def make_output():
    clean_file('s1.txt', '')
    get_prn(sorted(domains, key=domains.get, reverse=True)[:out_lines], domains)
    # print()
    get_prn(('GET', 'POST', 'OVERALL'), total)
    write_file('s1.txt', "{:>16s}: {:4d}".format('UNIQUE DOMAINS', len(unique)))
    # print("{:>16s}: {:4d}".format('UNIQUE DOMAINS', len(unique)))
    # print(40 * '=')


def main():
    global lines
    with open(logfile) as log:
        m_data = log.readlines()[lines:]
    for line in m_data:
        lines += 1
        line_log = line.split()
        if not line_log:
            continue
        t = (float(line_log[-1]) if re.match('[0-9]', line_log[-1]) else 0.0)
        d = clean(line_log[1].lower())
        if line_log[8] in ('200', '301'):
            unique.add(d)
        if not (re.match('cp(?:[0-9]|11)\.', d)):
            fill_dict(domains, d, t)
        g = line_log[5].strip('"')
        if g in ('GET', 'POST'):
            fill_dict(total, g, t)
        fill_dict(total, 'OVERALL', t)
    make_output()


def write_file(name_file, arg):
    with open(name_file, 'a') as writes_file:
        writes_file.write(arg + '\n')


def clean_file(name_file, arg):
    with open(name_file, 'w') as writes_files:
        writes_files.write(arg)

domains = {}
unique = set()
total = {}
lines = 0

logfile = "log.log"
out_fmt = "{:>16s}: {:4d}{:8.0f}{:8.3f}"
out_lines = 10
sleep_time = 5.0

while True:
    if datetime.strftime(datetime.now(), "%H:%M") == '23:59':
        domains.clear()
        total.clear()
        unique.clear()
        lines = 0
        sleep(900)
    else:
        main()
        sleep(sleep_time)
