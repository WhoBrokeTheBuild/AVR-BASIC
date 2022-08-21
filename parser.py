
import re

from tokens import *

def parse(data):
    tokens = []

    basic = re.compile(r"'.*|([_a-zA-Z][_a-zA-Z0-9]*|\$?%?[0-9]+|\".*\"|<>|<<|>>|<=|>=|[\(\)\+\-\/\*=\?,<>])")

    matches = basic.findall(data)
    for match in matches:
        if match == '':
            continue

        token = parse_token(match)
        if not token:
            break
        
        tokens.append(token)
    
    return tokens
