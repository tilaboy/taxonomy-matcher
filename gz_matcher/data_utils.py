import re

SEPERATOR = r'[a-zA-Z0-9\_]+|[^a-zA-Z0-9\_\s]+'
SEPERATOR_REGEXP = re.compile(SEPERATOR)

def prepare_from_gz(gz_file):
    patterns = []
    with open(gz_file, 'rt') as gz_fh:
        for line in gz_fh:
            add_pattern_from_line(patterns, line)
    return patterns

def add_pattern_from_line(patterns, line):
    if line.startswith('#') or re.match(r'^\W+$', line):
        pass
    else:
        patterns.append(tokenize(line.rstrip(), pos_info=False))
    return

def count_tokens(string):
    tokens = tokenize(string, pos_info=False)
    return len(tokens)

def normalize(string):
    return string.lower()

def tokenize(text, pos_info=True):
    tokens = []
    for match in SEPERATOR_REGEXP.finditer(normalize(text)):
        if pos_info:
            tokens.append([match.group(), match.start(), match.end() - 1])
        else:
            tokens.append(match.group())

    return tokens
