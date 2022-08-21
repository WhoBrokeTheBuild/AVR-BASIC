import sys

from compiler import *

for filename in sys.argv[1:]:
    compile(filename)