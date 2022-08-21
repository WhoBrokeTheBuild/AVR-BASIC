
import re

from tokens import *

def parse_token(string):
    token = OperatorToken.parse(string)
    if token:
        return token
        
    token = KeywordToken.parse(string)
    if token:
        return token
        
    token = NameToken.parse(string)
    if token:
        return token
        
    token = StringLiteralToken.parse(string)
    if token:
        return token
        
    token = NumericLiteralToken.parse(string)
    if token:
        return token
    
    print("Failed to parse token '{}'".format(string))
    return None

def parse(data):
    tokens = []

    basic = re.compile(r"\s*'.*|([_a-zA-Z][\._a-zA-Z0-9]*|\$?%?[0-9A-F]+|\".*\"|\*\*|\*\/|\/\/|&\/|\|\/|\^\/|<<|>>|<>|<=|>=|[\(\)\+\-\/\*=<>\?,\n])")

    matches = basic.findall(data)
    for match in matches:
        if match == '':
            continue

        token = parse_token(match)
        if not token:
            break
        
        tokens.append(token)
    
    return tokens
