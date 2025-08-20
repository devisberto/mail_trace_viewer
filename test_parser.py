import parser


def test_extract_hops_bracket_ip():
    headers = "Received: from [203.0.113.1] by example.com;\n\n"
    hops = parser.extract_hops(headers)
    assert hops[0]['hostname'] == '203.0.113.1'
    assert hops[0]['ip'] == '203.0.113.1'

