import re

class Tokenizer():
    def __init__(self, regexp=None):
        if regexp is not None:
            self.regexp = regexp
        else:
            self.regexp = re.compile(r'[a-zA-Z0-9\_]+|[^a-zA-Z0-9\_\s]+')


    def tokenize(self, text, pos_info=True):
        tokens = []
        for match in self.regexp.finditer(text):
            if pos_info:
                tokens.append([match.group(), match.start(), match.end() - 1])
            else:
                tokens.append(match.group())

        return tokens
