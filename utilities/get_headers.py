def get_headers(headers: list[str]) -> list[tuple[str, str]]:
    res = []
    
    for h in headers:
        header = h.split(': ')
        res.append((header[0].lower(), header[1].lower()))
    
    return res