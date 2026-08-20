import re


def check_visit(vis: str):
    return re.match(r"([a-z]{2})([1-9]\d*)-([1-9]\d*)", vis)
