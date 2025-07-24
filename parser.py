"""
Email Trace App - Web application to analyze email headers and display routing and reputation information.

Copyright (C) 2025 Devis Berto

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import re
import socket
from email import message_from_string

def is_ip_address(value):
    try:
        socket.inet_pton(socket.AF_INET, value)
        return True
    except OSError:
        try:
            socket.inet_pton(socket.AF_INET6, value)
            return True
        except OSError:
            return False

def resolve_hostname(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.error:
        return ""

def extract_hops(raw_headers):
    msg = message_from_string(raw_headers)
    received_headers = msg.get_all('Received') or []
    hops = []
    for line in received_headers:
        match = re.search(r'from\s+(\S+)', line)
        if match:
            host = match.group(1)
            if is_ip_address(host):
                hops.append({
                    'hostname': host,
                    'ip': host,
                    'raw': line
                })
            else:
                resolved_ip = resolve_hostname(host)
                hops.append({
                    'hostname': host,
                    'ip': resolved_ip,
                    'raw': line
                })
    return hops[::-1]
