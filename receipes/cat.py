from syntax_sugar import *
from sys import argv


pipe(argv[1:]) | each(lambda filename: open(filename).read()) | concat | puts
