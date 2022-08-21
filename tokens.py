
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
    'IF' 'THEN', 'ELSE', 'ENDIF',
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
    '?', # sends "symbol = x"
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

control_operators = [
    '(',
    ')',
    ',', # hack?'
]

unary_operators = [
    '-', # negative
    '~', # not
    'SQR', # Square root unary operator
    'ABS', # Absolute value unary operator
    'SIN', # ... brads
    'COS', #
    'DCD', # set bit #
    'NCD', # get highest bit # + 1
]

binary_operators = [
    '=',
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
]

comparison_operators = [
    '=',
    '>',
    '<',
    '<>',
    '<=',
    '>=',
]

boolean_operators = [
    'NOT',
    'AND',
    'OR',
    'XOR',
]

operators = list(set(
    control_operators +
    unary_operators +
    binary_operators +
    comparison_operators +
    boolean_operators
))

class Token:
    pass

class KeywordToken(Token):

    def __init__(self, keyword):
        self.keyword = keyword

    def __repr__(self):
        return '<KeywordToken {} >'.format(self.keyword)

    @classmethod
    def parse(cls, string):
        string = string.upper()

        if string in keywords:
            return KeywordToken(string)
            
        return None

class OperatorToken(Token):
    
    def __init__(self, operator):
        self.operator = operator

    def __repr__(self):
        return '<OperatorToken {} >'.format(self.operator)

    @classmethod
    def parse(cls, string):
        string = string.upper()

        if string in operators:
            return OperatorToken(string)

        return None

class NameToken(Token):
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<NameToken {} >'.format(self.name)

    @classmethod
    def parse(cls, string):
        if len(string) >= 1 and len(string) <= 32:
            if string[0].isalpha() or string[0] == '_':
                return NameToken(string)

        return None

class LiteralToken(Token):
    
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '<LiteralToken type={} {} >'.format(type(self.value), self.value)

    @classmethod
    def parse(cls, string):

        if len(string) >= 3:
            if string[0] == '"' and string[-1] == '"':
                bytes = string[1:len(string) - 1].encode('ascii')
                return LiteralToken(bytes)

        if len(string) > 0:
            if string[0] == '$':
                return LiteralToken(int(string[1:], 16))
            elif string[0] == '%':
                return LiteralToken(int(string[1:], 2))
            else:
                return LiteralToken(int(string, 10))

        return None

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
        
    token = LiteralToken.parse(string)
    if token:
        return token
    
    print("Failed to parse token '{}'".format(string))
    return None