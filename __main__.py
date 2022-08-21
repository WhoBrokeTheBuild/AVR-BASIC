import sys

from parser import *
from compiler import *

for filename in sys.argv[1:]:
    file = open(filename)
    data = file.read()
    # data = preprocess(data)
    tokens = parse(data)
    compile(tokens)