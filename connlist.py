#!/usr/bin/env python
#
# Parse firewall log messages to present a short summary of TCP+UDP connections
#
# Version: 2.1
#
import re, sys
sys.path.append('lib/fw-regex')
from libfwregex import get_builtconn

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', \
						'Oct', 'Nov', 'Dec']

# Mapping of protocol number to name
protocols = {1: 'ICMP', 6: 'TCP', 17: 'UDP'}

# List of connections and timestamps
conns = {}
connFirst = {}
connLast = {}

for line in sys.stdin:
    data = get_builtconn(line)
    if data:
        # Unify protocol to uppercase name
        try:
            # Convert number to name
            pn = int(data['protocol'])
            data['protocol'] = protocols[pn]
        except:
            # Uppercase protocol name
            data['protocol'] = data['protocol'].upper()

        # Convert None to empty string if port number is missing (f.ex for ICMP)
        if not data['dport']:
            data['dport'] = ''

        # Create a connection hash: PROTO;FROMIP;TOIP;TOPORT
        conn = ';'.join([data['protocol'], data['src'], data['dst'], data['dport']])

        # Create a timestamp
        if 'year' in data:
            timestamp = '-'.join([data['year'], data['month'], data['day']]) + \
                ' ' + data['time']
        else:
            # This timestamp is incomplete, no year info makes it impossible to 
            # piece something together. Just use month, day and time in those cases.
            timestamp = '-'.join([data['month'], data['day']]) + ' ' + data['time']

        if conn in conns.keys():
            conns[conn] = conns[conn] + 1
            if timestamp < connFirst[conn]:
                connFirst[conn] = timestamp
            if timestamp > connLast[conn]:
                connLast[conn] = timestamp
        else:
            conns[conn] = 1
            connFirst[conn] = timestamp
            connLast[conn] = timestamp

# Sort list of conns
entries = conns.keys()
entries.sort(key=lambda conn: ' '.join(conn.split(';')[2:4]))

# Print header
print '%6s %4s  %-15s %-14s %-5s %-19s  %-19s' % ('COUNT', 'PROTO', \
	'FROM IP', 'TO IP', 'PORT', 'FIRST SEEN', 'LAST SEEN')

# Print connection table
for conn in entries:
	proto, fromIP, toIP, toport = conn.split(';')
	print '%6d %4s %15s  %15s %-5s %19s  %19s' % (conns[conn], proto, fromIP, \
			toIP, toport, connFirst[conn], connLast[conn])

