import re


def validate_uuid(s):
    s = re.sub(r"[^a-fA-F0-9-]", "", s)
    return s
