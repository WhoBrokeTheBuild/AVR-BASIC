
from tokens import *

class TokenIterator:

    def __init__(self, tokens):
        self.tokens = tokens

    def peek(self, offset = 0):
        if offset >= len(self.tokens):
            return None
        return self.tokens[offset]

    def pop(self):
        if len(self.tokens) == 0:
            return None

        token = self.tokens[0]
        self.tokens = self.tokens[1:]
        return token

    def empty(self):
        return len(self.tokens) == 0

def compile(tokens):

    assembly = '''
.device ATMega328P

.cseg
.org 0
    rjmp $

'''

    registerMasks = [ 0x00 ] * 32
    registerMap = [ ]
    variableMap = { }

    def add_mappings(name, size):
        if size == 16:
            return add_mappings(name + '_LOW', 8) + add_mappings(name + '_HIGH', 8)
        elif size == 8:
            for index in range(len(registerMasks)):
                if registerMasks[index] == 0x00:
                    registerMasks[index] = 0xFF
                    registerMap.append({
                        'name': name,
                        'size': size,
                        'index': index,
                        'mask': 0xFF
                    })
                    return registerMap[-1:]
        elif size == 4:
            for index in range(len(registerMasks)):
                mask = 0
                for testMask in [ 0x0F, 0xF0 ]:
                    if (registerMasks[index] & testMask) == 0:
                        mask = testMask
                        break

                if mask != 0:
                    registerMasks[index] |= mask
                    registerMap.append({
                        'name': name,
                        'size': size,
                        'index': index,
                        'mask': mask
                    })
                    return registerMap[-1:]
        elif size == 1:
            for index in range(len(registerMasks)):
                mask = 0
                for testMask in [ 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80 ]:
                    if (registerMasks[index] & testMask) == 0:
                        mask = testMask
                        break

                if mask != 0:
                    registerMasks[index] |= mask
                    registerMap.append({
                        'name': name,
                        'size': size,
                        'index': index,
                        'mask': mask
                    })
                    return registerMap[-1:]

    def get_mappings(name):
        mappings = []
        for mapping in registerMap:
            if mapping['name'] in ( name, name + '_LOW', name + '_HIGH' ):
                mappings.append(mapping)
        return mappings

    add_mappings('IN', 16)
    add_mappings('OUT', 16)
    add_mappings('DIR', 16)

    tokens = TokenIterator(tokens)

    while not tokens.empty():
        token1 = tokens.pop()
        token2 = tokens.peek(0)
        token3 = tokens.peek(1)

        if type(token1) == NameToken:
            if type(token2) == KeywordToken:
                if token2.keyword == 'CON':
                    if type(token3) == LiteralToken:
                        assembly += '.equ {} = {}\n'.format(token1.name, token3.value)
                    else:
                        raise SyntaxError('CON must have a literal, not {}'.format(token3))

                elif token2.keyword == 'VAR':
                    if type(token3) == KeywordToken:
                        mappings = []
                        if token3.keyword == 'WORD':
                            mappings = add_mappings(token1.name, 16)
                        elif token3.keyword == 'BYTE':
                            mappings = add_mappings(token1.name, 8)
                        elif token3.keyword == 'NIB':
                            mappings = add_mappings(token1.name, 4)
                        elif token3.keyword == 'BIT':
                            mappings = add_mappings(token1.name, 1)
                        else:
                            raise SyntaxError('VAR must have a type or another variable, not {}'.format(token3))

                        for mapping in mappings:
                            assembly += '.def {} = r{} ;; mask=0x{:02X}\n'.format(mapping['name'], mapping['index'], mapping['mask'])

                    elif type(token3) == NameToken:
                        variableMap[token1.name] = token3.name
                        assembly += ';; alias {} = {}\n'.format(token1.name, token3.name)
                    else:
                        raise SyntaxError('VAR must have a type or another variable, not {}'.format(token3))
    
    print(assembly)

    with open('test.asm', 'wt') as test:
        test.write(assembly)