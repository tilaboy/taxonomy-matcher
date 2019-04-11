import re

def normalize(string):
    return string.lower()

def validate_pattern(pattern, blacklist=[]):
    valid = True
    if not has_content(pattern):
        valid = False
    elif normalize(pattern) in blacklist:
        valid = False
    return valid

def has_content(pattern):
    is_content_line = True
    if pattern.startswith('#') or re.match(r'^\W*$', pattern):
        is_content_line = False
    return is_content_line


def from_file_to_list(file):
    lines = []
    with open(file) as fh:
        for line in file:
            line = line.rstrip()
            if has_content(line):
                lines.append(line)
    return lines
