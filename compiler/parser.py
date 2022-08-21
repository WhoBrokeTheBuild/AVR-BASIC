
from .tokens import *

def parse(data):
    tokens = TokenQueue()

    data = data + '\n'

    token_classes = [
        NewlineToken,
        CommaToken,
        CommentToken,
        ColonToken,
        KeywordToken,
        OperatorToken,
        NameToken,
        NumericLiteralToken,
        StringLiteralToken,
    ]

    while len(data) > 0:
        for cls in token_classes:
            token, span = cls.match(data)
            if token:
                data = data[span[1]:]
                print(token, len(data))
                tokens.append(token)
                break

    return tokens
