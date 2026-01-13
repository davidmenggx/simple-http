from pathlib import Path

import responses

BASE_DIR = Path('public').resolve()

def get(path: str) -> bytes:
    if path[0] == '/':
        path = path[1:]

    requested_path = (BASE_DIR / path).resolve()

    if BASE_DIR in requested_path.parents or BASE_DIR == requested_path:
        if requested_path.exists() and requested_path.is_file():
            try:
                with open(requested_path, 'rb') as f:
                    content = f.read()
                    return content
            except FileNotFoundError:
                return responses.not_found()
        else:
            return responses.not_found()
    else:
        return responses.forbidden()