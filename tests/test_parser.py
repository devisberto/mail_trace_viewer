import importlib.util
from pathlib import Path
from unittest.mock import patch

# Dynamically import the parser module from the repository root
spec = importlib.util.spec_from_file_location('parser', Path(__file__).resolve().parent.parent / 'parser.py')
parser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parser)

def test_extract_hops_resolvable_hostname():
    headers = "Received: from mail.example by example.com;\n\n"
    with patch.object(parser, 'resolve_hostname', return_value='127.0.0.1') as mock_resolve:
        hops = parser.extract_hops(headers)
        mock_resolve.assert_called_once_with('mail.example')
    assert hops[0]['hostname'] == 'mail.example'
    assert hops[0]['ip'] == '127.0.0.1'

def test_extract_hops_unresolvable_hostname():
    headers = "Received: from unknown.example by example.com;\n\n"
    with patch.object(parser, 'resolve_hostname', return_value='') as mock_resolve:
        hops = parser.extract_hops(headers)
        mock_resolve.assert_called_once_with('unknown.example')
    assert hops[0]['hostname'] == 'unknown.example'
    assert hops[0]['ip'] == ''

def test_extract_hops_ipv6_address():
    headers = "Received: from [2001:db8::1] by example.com;\n\n"
    hops = parser.extract_hops(headers)
    assert hops[0]['hostname'] == '2001:db8::1'
    assert hops[0]['ip'] == '2001:db8::1'
