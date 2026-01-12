from exceptions import ParseError

def get_request_line(request: str) -> tuple[tuple[str, str, str], list[str]]: # returns ((method, path, version), rest of text)
    request_line = request.split('\r\n')[0]
    
    if len(request_line.split()) != 3:
        raise ParseError
    
    method, path, protocol_version = request_line.split()

    headers = request_line = request.split('\r\n')[1:]

    return ((method, path, protocol_version), headers)