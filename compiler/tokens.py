
from ast import pattern
from msilib import type_key
import re
from xml.etree.ElementTree import Comment

definition_keywords = [
    'CON', # constant
    'VAR', # variable (register?)
    'PIN', # constant-ish
    # 'DATA', # 
]

numeric_keywords = [
    'LOOKUP', # look up data in table by offset
    'LOOKDOWN', # reverse lookup?
    'RANDOM', # generate pseudo-random number
]

io_keywords = [
    'INPUT', # pinMode
    'OUTPUT', # pinMode
    'REVERSE', # pinMode(!mode)
    'LOW', # digitalWrite
    'HIGH', # digitalWrite
    'TOGGLE', # digitalWrite(!current)
    'PULSIN',
    'PULSOUT',
    'BUTTON',
    'COUNT',
    'XOUT', # generate X-10 power line control codes
    'SERIN',
    'SEROUT', # Serial.print
    'SHIFTIN',
    'SHIFTOUT',
    'PWM', # output pulse width modulation
    'RCTIME', # measure variable resistance
    'FREQOUT', # output frequency
    'DTMFOUT', # output DTMF tone
    'DEBUG', # Serial.print
    'DEBUGIN',
]

control_keywords = [
    'BRANCH',
    'IF', 'THEN', 'ELSE', 'ENDIF',
    'GOTO', # jump
    'GOSUB', # call
    'ON', # used with goto/gosub, a lot like branch
    'RETURN', # return
    'SELECT', 'CASE',
    'STOP', # end program (jp $?)
    'DO', 'LOOP',
    'EXIT', # break
    'FOR', 'NEXT', 'TO', 'STEP',
    'END', # end program (jp $?), but wait for PC to connect??
    'NAP', # ???
    'PAUSE', # sleep
    'SLEEP', 
]

type_keywords = [
    'BIT',
    'NIB',
    'BYTE',
    'WORD',
]

access_keywords = [
    'HIGHBYTE',
    'LOWBYTE',
    'LOWNIB',
    'HIGHNIB',
    'LOWBIT',
    'HIGHBIT',
]

access_keywords += [ 'BIT{}'.format(i) for i in range(1, 17) ]
access_keywords += [ 'NIB{}'.format(i) for i in range(1, 5) ]
access_keywords += [ 'BYTE{}'.format(i) for i in range(1, 3) ]

debug_format_keywords = [
    'REP', # repeat byte x times, e.g. REP "A"\5 sends "AAAAA"
    'ASC', # Changes ? to display "symbol = 'x'", converting x to an ascii character
    'STR', # sends byte array as string, can be limited, e.g. STR array\5 sends 5 characters from the array
    'DEC',
    'SDEC',
    'HEX',
    'SHEX',
    'IHEX', # with the prefix $
    'ISHEX',
    'BIN',
    'SBIN',
    'IBIN', # with the prefix %
    'ISBIN',
]

# all fixed-length formatters will prefix with 0s if needed, and truncate to the number of digits specified
debug_format_keywords += [ 'DEC{}'.format(i) for i in range(1, 6) ]
debug_format_keywords += [ 'SDEC{}'.format(i) for i in range(1, 6) ]
debug_format_keywords += [ 'HEX{}'.format(i) for i in range(1, 5) ]
debug_format_keywords += [ 'SHEX{}'.format(i) for i in range(1, 5) ]
debug_format_keywords += [ 'IHEX{}'.format(i) for i in range(1, 5) ]
debug_format_keywords += [ 'ISHEX{}'.format(i) for i in range(1, 5) ]
debug_format_keywords += [ 'BIN{}'.format(i) for i in range(1, 17) ]
debug_format_keywords += [ 'SBIN{}'.format(i) for i in range(1, 17) ]
debug_format_keywords += [ 'IBIN{}'.format(i) for i in range(1, 17) ]
debug_format_keywords += [ 'ISBIN{}'.format(i) for i in range(1, 17) ]

debug_literal_keywords = [
    # 'CLS', # $00, clear screen
    'HOME', # $01, place cursor in upper-left corner
    # 'CRSRXY', # $02, place cursor to coordinates
    # 'CRSRLF', # $03, move cursor one left
    # 'CRSRRT', # $04, move cursor one right
    # 'CRSRUP', # $05, move cursor one up
    # 'CRSRDN', # $06, move cursor one down
    'BELL', # \a
    'BKSP', # \b
    'TAB', # \t
    'LF', # \n
    # 'CLREOL', # clear line contents right of the cursor
    # 'CLRDN', # clear screen contents below the cursor
    'CR', # \r
    # 'CRSRX', # move cursor to x coordinate
    # 'CRSRY', # move cursor to y coordinate
]

keywords = list(set(
    definition_keywords +
    numeric_keywords +
    io_keywords +
    control_keywords +
    type_keywords +
    access_keywords +
    debug_format_keywords +
    debug_literal_keywords
))

unary_operators = [
    '?', # debug format, sends "symbol = x"
    '-', # negative
    '~', # not
    'SQR', # Square root unary operator
    'ABS', # Absolute value unary operator
    'SIN', # ... brads
    'COS', #
    'DCD', # set bit #
    'NCD', # get highest bit # + 1
    'NOT',
]

binary_operators = [
    '=',
    '>',
    '<',
    '<>',
    '<=',
    '>=',
    '+',
    '-',
    '*',
    '**', # upper 16 of multiplication
    '*/', # multiply by 8 bit integer, 8 bit fraction (BCD?)
    '/',
    '//', # modulus
    '<<', # bit shift left
    '>>', # bit shift right
    '&', # bitwise and
    '&/', # bitwise and not
    '|', # bitwise or
    '|/', # bitwise or not
    '^', # bitwise xor
    '^/', # bitwise xor not
    'ATN', # arctangent
    'HYP', # hypotenuse
    'MIN',
    'MAX',
    'DIG', # digit of number?
    'REV', # reverse bits???
    'AND',
    'OR',
    'XOR',
]

operators = list(set(
    unary_operators +
    binary_operators
))

class Token:
    @classmethod
    def match(cls, string):
        return False

class NewlineToken(Token):

    pattern = re.compile(r'^\s*\n')

    def __repr__(self):
        return '<NewlineToken>'

    @classmethod
    def match(cls, string):
        result = cls.pattern.match(string)
        if result:
            return NewlineToken(), result.span()
        return None, None

class CommaToken(Token):

    pattern = re.compile(r'^\s*,')

    def __repr__(self):
        return '<CommaToken>'

    @classmethod
    def match(cls, string):
        result = cls.pattern.match(string)
        if result:
            return CommaToken(), result.span()
        return None, None

class ColonToken(Token):

    pattern = re.compile(r'^\s*:')

    def __repr__(self):
        return '<ColonToken>'

    @classmethod
    def match(cls, string):
        result = cls.pattern.match(string)
        if result:
            return ColonToken(), result.span()
        return None, None

class CommentToken(Token):
    def __init__(self, comment):
        self.comment = comment

    def __repr__(self):
        return '<CommentToken comment="{}" >'.format(self.comment)

    pattern = re.compile(r'^\s*\'(.*)')

    @classmethod
    def match(cls, string):
        result = cls.pattern.match(string)
        if result:
            match = result[1]
            return CommentToken(match), result.span()
        return None, None

class KeywordToken(Token):
    def __init__(self, keyword):
        self.keyword = keyword

    def is_definition(self):
        return self.keyword in definition_keywords

    def is_io(self):
        return self.keyword in io_keywords

    def is_control(self):
        return self.keyword in control_keywords

    def is_type(self):
        return self.keyword in type_keywords

    def is_access(self):
        return self.keyword in access_keywords

    def is_debug_format(self):
        return self.keyword in debug_format_keywords

    def is_debug_literal(self):
        return self.keyword in debug_literal_keywords

    def __repr__(self):
        return '<KeywordToken keyword={} >'.format(self.keyword)

    pattern = re.compile(r'^\s*([a-zA-Z]+)')

    @classmethod
    def match(cls, string):
        result = cls.pattern.match(string)
        if result:
            match = result[1].upper()
            if match in keywords:
                return KeywordToken(match), result.span()
        return None, None

class NameToken(Token):
    def __init__(self, name):
        parts = name.split('.', 1)
        self.name = parts[0]

        self.suffix = ''
        if len(parts) > 1:
            self.suffix = parts[1]

    pattern = re.compile(r'^\s*([_a-zA-Z][\._a-zA-Z0-9]*)')

    def __repr__(self):
        return '<NameToken name={} >'.format(self.name)

    @classmethod
    def match(cls, string):
        result = cls.pattern.match(string)
        if result:
            match = result[1]
            # TODO: 32 character limit
            return NameToken(match), result.span()
        return None, None

class StringLiteralToken(Token):
    
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '<StringLiteralToken value="{}" >'.format(self.value)

    pattern = re.compile(r'^\s*(\".*\")')

    @classmethod
    def match(cls, string):
        result = cls.pattern.match(string)
        if result:
            match = result[1]
            return StringLiteralToken(match), result.span()
        return None, None

class NumericLiteralToken(Token):
    
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '<NumericLiteralToken value:dec={:05d} value:hex=${:04X} value:bin=%{:016b} >'.format(self.value, self.value, self.value)

    pattern = re.compile(r'^\s*([0-9]+|\$[0-9A-F]+|\%[0-1]+)')

    @classmethod
    def match(cls, string):
        result = cls.pattern.match(string)
        if result:
            match = result[1]

            value = None
            if match[0] == '$':
                value = int(match[1:], 16)
            elif match[0] == '%':
                value = int(match[1:], 2)
            else:
                value = int(match, 10)

            if value:
                return NumericLiteralToken(value), result.span()
        return None, None

class OperatorToken(Token):
    def __init__(self, operator):
        self.operator = operator
    
    def is_assignment(self):
        return self.operator == '='

    def is_debug_format(self):
        return self.operator == '?'

    def is_unary(self):
        return self.operator in unary_operators

    def is_binary(self):
        return self.operator in binary_operators

    def __repr__(self):
        return '<OperatorToken operator="{}" >'.format(self.operator)

    pattern = re.compile(r'^\s*(<>|<=|>=|<<|>>|\*\*|\*\/|\/\/|&\/|\|\/|\^\/|SQR|ABS|SIN|COS|DCD|NCD|AND|OR|XOR|[\?\-~=<>\+\-\*\/&\|\^])')

    @classmethod
    def match(cls, string):
        result = cls.pattern.match(string)
        if result:
            match = result[1]
            return OperatorToken(match[0]), result.span()
        return None, None

class TokenQueue(list):
    """
    FIFO queue of tokens to process
    """

    def __init__(self, tokens=list()):
        self.tokens = tokens

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

    def peek(self, offset = 0, count = 1):
        if count == 1:
            if offset >= len(self.tokens):
                return None

            return self.tokens[offset]
        else:
            if offset >= len(self.tokens):
                return [ None ] * count

            if offset + count >= len(self.tokens):
                remaining = len(self.tokens) - (offset + count)
                return self.tokens[offset:] + ([ None ] * remaining)

            return self.tokens[offset:offset + count]

    def pop(self, count = 1):
        if count == 1:
            if len(self.tokens) == 0:
                return None

            token = self.tokens[0]
            self.tokens = self.tokens[1:]
            return token
        else:
            if count >= len(self.tokens):
                tokens = self.tokens[:count]
                self.tokens = []
                remaining = count - len(tokens)
                return tokens + ([ None ] * remaining)

            tokens = self.tokens[:count]
            self.tokens = self.tokens[count:]
            return tokens

    def empty(self):
        return len(self.tokens) == 0

