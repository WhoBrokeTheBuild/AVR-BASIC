
Newline = \n

Comma = ,

Period = .

Colon = :

OpenParen = (

CloseParen = )

Comment = '(.*)

StringLiteral = "(.*)"

NumericLiteral = ([0-9]+|\$[0-9A-F]+|\%[0-1]+)

Name = ([_a-zA-Z][_a-zA-Z0-9]*)

Access = 
    Period
    (
        HIGHBYTE | LOWBYTE | BYTE# |
        HIGHNIB | LOWNIB | NIB# |
        HIGHBIT | LOWBIT | BIT#
    )

Variable =
    Name[ .Access ][ OpenParen Expression CloseParen ]

Type = ( BIT | BIT(#) | NIB | NIB(#) | BYTE | BYTE(#) | WORD | WORD(#) )

Label = Name Colon

Definition = 
    Name CON Expression |
    Name VAR (Type | Variable) |
    Name PIN Expression

Argument =
    Name |
    StringLiteral |
    Expression

ArgumentList = 
    Argument [ Comma Argument ]...

Expression = 
    Variable |
    NumericLiteral |
    OpenParen Expression CloseParen
    UnaryOperator Expression |
    Expression BinaryOperator Expression

Condition =
    [ NOT ] Expression |
    OpenParen Condition CloseParen
    Condition ComparisonOperator Condition

CommandKeyword =
    a bunch of shit

Command = 
    CommandKeyword [ ArgumentList ]

Command_ON = 
    ON Expression ( GOTO | GOSUB ) ArgumentList

CASE_Condition =
    Expression |
    ComparisonOperator Expression |
    Expression TO Expression
    # ???

CASE_ConditionList = 
    CASE_Condition [ Comma CASE_Condition ]...

Command_CASE =
    CASE CASE_ConditionList Statement...

Command_SELECT = 
    SELECT Expression [ Command_Case ]... ENDSELECT

Command_ELSEIF = 
    ELSEIF Condition THEN Statement...

Command_ELSE = 
    ELSE Statement...

Command_IF = 
    IF Condition THEN Name |
    IF Condition THEN Statement... [ Command_ELSEIF ]... [ Command_ELSE ] ENDIF

Command_DO =
    DO Statement... LOOP

# max of 16 nested loops
Command_FOR = 
    FOR Variable = Expression TO Expression [ STEP Expression ] Statement... NEXT [ Variable ???? ]

DebugFormat =
    ? \
    DEC | SDEC | DEC# | SDEC# |
    HEX | SHEX | IHEX | ISHEX | HEX# | SHEX# | IHEX# | ISHEX# |
    BIN | SBIN | IBIN | ISBIN | BIN# | SBIN# | IBIN# | ISBIN# |
    REP | ASC | STR

DebugLiteral = 
    HOME | BELL | BKSP | TAB | LF | CR

DebugFormatLength = \\[0-9]+

DebugArgument =
    [ DebugFormat ] ( Argument | DebugLiteral ) [ DebugFormatLength ]

DebugArgumentList =
    DebugArgument [ Comma DebugArgument ]

Command_DEBUG = 
    DEBUG DebugArgumentList

Statement = 
    Definition |
    Expression |
    Command |
    Command_ON |
    Command_SELECT |
    Command_IF |
    Command_DO |
    Command_FOR |
    Command_DEBUG