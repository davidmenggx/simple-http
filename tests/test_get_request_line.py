import pytest

from utilities import get_request_line

def test_valid_request():
    valid_request = "POST /api/public_file.txt HTTP/1.1\r\nHost: api.example.com\r\nContent-Type: application/json\r\nContent-Length: 73"
    assert get_request_line(valid_request) == (('POST', '/api/public_file.txt', 'HTTP/1.1'), ['Host: api.example.com', 'Content-Type: application/json', 'Content-Length: 73'])

def test_invalid_request_line():
    invalid_request = "POST /api/public_file.txt\r\nHost: api.example.com\r\nContent-Type: application/json\r\nContent-Length: 73"
    with pytest.raises(ValueError):
        get_request_line(invalid_request)