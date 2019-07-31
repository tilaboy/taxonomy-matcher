'''Data Utils'''
import re


def normalize(string):
    '''
    normalize the input string

    params:
        - text string: (string)

    output:
        - normalized text string: (string)
    '''
    return string.lower()


def from_file_to_list(file):
    '''
    read content of the file, and return lines which have cotent
        - not a comment line (start with #)
        - contain alphanumber character

    params:
        - file: filename (string)

    output:
        - a list of validated lines: (list)
    '''
    lines = []
    with open(file, 'r+', encoding="utf-8") as handler:
        for line in handler:
            line = line.rstrip()
            if has_content(line):
                lines.append(line)
    return lines


def fetch_node_text(record, xpath):
    '''
    fetch text of a node in the record

    params:
        - record: ElementTree object
        - xpath: xpath string

    output:
        - text of the node specified by xpath, return None if no node found
    '''
    node_text = None

    node = record.find(xpath)
    if node is not None:
        node_text = node.text

    return node_text


def has_content(pattern):
    is_content_line = True
    if pattern.startswith('#') or re.match(r'^\W*$', pattern):
        is_content_line = False
    return is_content_line
