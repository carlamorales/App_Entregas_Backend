import re


RUT_REGEXES = [
re.compile(r"^[0-9]{1,2}\.[0-9]{3}\.[0-9]{3}-[0-9Kk]$"),
re.compile(r"^[0-9]{7,8}-[0-9Kk]$")
]


def is_valid_rut(rut: str) -> bool:
    if not rut:
        return False
    return any(rx.match(rut) for rx in RUT_REGEXES)