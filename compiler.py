
import math
from tokenize import tabsize

from tokens import *

def rad2brad(rad):
    return round((math.degrees(rad) / 360) * 255)

def brad2rad(brad):
    return math.radians((brad / 255) * 360)

class TokenIterator(list):

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

    def push(self, tokens):
        if type(tokens) == list:
            self.tokens = tokens + self.tokens
        else:
            self.tokens.insert(0, tokens)

    def skip(self, amount):
        if amount >= len(self.tokens):
            self.tokens = []
        else:
            self.tokens = self.tokens[amount:]

    def empty(self):
        return len(self.tokens) == 0

class NumericExpression:
    def __init__(self, tokens, variableMap, paren=False):
        self.tokens = TokenIterator()
        while not tokens.empty():
            token = tokens.peek()
            if type(token) == NameToken:
                if token.name in variableMap:
                    mapEntry = variableMap[token.name]
                    if mapEntry['type'] == 'CON':
                        tokens.pop()
                        self.tokens.push(NumericLiteralToken(mapEntry['value']))
                    else:
                        self.tokens.push(tokens.pop())
            elif type(token) == NumericLiteralToken:
                self.tokens.append(tokens.pop())
            elif type(token) == OperatorToken:
                if token.operator == '(':
                    tokens.pop()
                    self.tokens.append(NumericExpression(tokens, variableMap, True))
                elif token.operator == ')':
                    tokens.pop()
                    if paren:
                        paren = False
                    else:
                        raise SyntaxError('Unexpected closing parenthesis')
                elif token.operator == '\n' or token.operator == ',':
                    break
                else:
                    self.tokens.append(tokens.pop())
            else:
                break

        if paren:
            raise SyntaxError('Unbalanced parenthesis')

        if len(self.tokens) > 0:
            if type(self.tokens[-1]) == OperatorToken:
                raise SyntaxError('Expressions cannot end with operators')

    def __repr__(self):
        self.print()

    def print(self, depth=0):
        for token in self.tokens:
            if type(token) == NumericExpression:
                token.print(depth + 1)
            else:
                print(('  ' * depth) + repr(token))

    def constant(self):
        for token in self.tokens:
            if type(token) == NumericExpression:
                if not token.constant():
                    return False
            elif type(token) != NumericLiteralToken and type(token) != OperatorToken:
                return False
        return True

    def evaluate(self):
        if not self.constant():
            return
        
        while not self.tokens.empty():
            token1 = self.tokens.peek(0)
            token2 = self.tokens.peek(1)
            token3 = self.tokens.peek(2)
                
            if type(token1) == OperatorToken:
                if type(token2) == NumericLiteralToken:
                    if token1.operator in unary_operators or token1.operator == 'NOT':
                        self.tokens.skip(2)

                        if token1.operator == '-':
                            token2.value *= -1
                            self.tokens.push(token2)
                        elif token1.operator == 'SQR':
                            token2.value = round(math.sqrt(token2.value))
                            self.tokens.push(token2)
                        elif token1.operator == 'ABS':
                            token2.value = abs(token2.value)
                            self.tokens.push(token2)
                        elif token1.operator == 'SIN':
                            angle = brad2rad(token2.value)
                            token2.value = round(math.sin(angle))
                            self.tokens.push(token2)
                        elif token1.operator == 'COS':
                            angle = brad2rad(token2.value)
                            token2.value = round(math.cos(angle))
                            self.tokens.push(token2)
                        elif token1.operator == 'DCD':
                            token2.value = (1 << token2.value)
                            self.tokens.push(token2)
                        elif token1.operator == 'NCD':
                            bits = '{:016b}'.format(token2.value)
                            bits = bits[::-1]
                            token2.value = bits.find('1') + 1
                            self.tokens.push(token2)
                        elif token1.operator == 'NOT':
                            pass

                        continue

                raise SyntaxError('Malformed expression')
            
            elif type(token1) == NumericLiteralToken:
                if type(token2) == OperatorToken:
                    if token2.operator in binary_operators or token2.operator in comparison_operators:
                        if type(token3) == NumericLiteralToken:
                            # COMPILE TIME MATH HERE WE GO
                            if token2.operator == '=':
                                raise SyntaxError('Cannot assign value to literal')
                            elif token2.operator == '+':
                                token1.value += token3.value
                            elif token2.operator == '-':
                                token1.value -= token3.value
                            elif token2.operator == '*':
                                token1.value *= token3.value
                            elif token2.operator == '**':
                                tmp = token1.value * token3.value
                                token1.value = (tmp & 0xFFFF0000) >> 16
                            elif token2.operator == '*/':
                                tmp = token1.value * token3.value
                                token1.value = (tmp & 0x00FFFF00) >> 8
                            elif token2.operator == '/':
                                token1.value /= token3.value
                            elif token2.operator == '//':
                                token1.value %= token3.value
                            elif token2.operator == '<<':
                                token1.value <<= token3.value
                            elif token2.operator == '>>':
                                token1.value >>= token3.value
                            elif token2.operator == '&':
                                token1.value &= token3.value
                            elif token2.operator == '&/':
                                token1.value &= ~token3.value
                            elif token2.operator == '|':
                                token1.value |= token3.value
                            elif token2.operator == '|/':
                                token1.value |= ~token3.value
                            elif token2.operator == '^':
                                token1.value ^= token3.value
                            elif token2.operator == '^/':
                                token1.value ^= ~token3.value
                            elif token2.operator == 'ATN':
                                angle = math.atan2(token3.value, token1.value)
                                token1.value = rad2brad(angle)
                            elif token2.operator == 'HYP':
                                hyp = math.sqrt((token1.value * token1.value) + (token3.value * token3.value))
                                token1.value = round(hyp)
                            elif token2.operator == 'MIN':
                                token1.value = min(token1.value, token3.value)
                            elif token2.operator == 'MAX':
                                token1.value = max(token1.value, token3.value)
                            elif token2.operator == 'DIG': # ???
                                digits = '{:05d}'.format(abs(token1.value)) # TODO: check if abs() is correct
                                digit = digits[token3.value]
                                token1.value = int(digit, 10)
                            elif token2.operator == 'REV':
                                bits = '{:016b}'.format(token1.value)
                                bits = bits[-token3.value:]
                                bits = bits[::-1]
                                token1.value = int(bits, 2)

                            self.tokens.skip(3)
                            self.tokens.insert(0, token1)


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
        token1 = tokens.peek(0)

        if type(token1) == OperatorToken and token1.operator == '\n':
            tokens.skip(1)
            continue
    
        token2 = tokens.peek(1)
        token3 = tokens.peek(2)

        print(token1, token2, token3)

        # TODO: parenthesis
        if type(token1) == KeywordToken:
            if token1.keyword == 'PAUSE':
                duration = NumericExpression(tokens)
                if duration.constant():
                    assembly += 'load r#, {}\n'.format(duration.evaluate())
                    assembly += 'call PAUSE\n'
                else:
                    pass

        elif type(token1) == NameToken:
            if type(token2) == OperatorToken:
                if token2.operator == '=':
                    tokens.skip(1)
                    Expression(tokens)
            elif type(token2) == KeywordToken:
                if token2.keyword == 'CON':
                    if '.' in token1.name:
                        raise SyntaxError('CON definitions can not have access modifiers')

                    if token1.name in variableMap:
                        raise SyntaxError('Variable name {} already in use'.format(token1.name))

                    if type(token3) == NumericLiteralToken:
                        assembly += '.equ {} = {}\n'.format(token1.name, token3.value)
                        variableMap[token1.name] = {
                            'type': 'CON',
                            'value': token3.value
                        }
                    else:
                        raise SyntaxError('CON must have a literal, not {}'.format(token3))

                    tokens.skip(2)

                elif token2.keyword == 'VAR':
                    if '.' in token1.name:
                        raise SyntaxError('VAR definitions can not have access modifiers')
                        
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

                        tokens.skip(2)
                    elif type(token3) == NameToken:
                        variableMap[token1.name] = token3.name
                        assembly += ';; alias {} = {}\n'.format(token1.name, token3.name)

                        tokens.skip(2)
                    else:
                        raise SyntaxError('VAR must have a type or another variable, not {}'.format(token3))
                        
    
    print(assembly)

    with open('test.asm', 'wt') as test:
        test.write(assembly)