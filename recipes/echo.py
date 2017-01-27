from syntax_sugar import *
from sys import argv

pipe(argv[1:]) | ' '.join | print | END
