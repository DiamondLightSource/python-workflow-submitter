import re


def check_visit(vis: str):
    return re.match(r"[a-zA-Z][a-zA-Z]\d\d\d\d\d-\d", vis)
