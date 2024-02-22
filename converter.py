#!/usr/bin/env python3
import sys
import pathlib

from touchstone_parser import *
from touchstone_writer import *

if len(sys.argv) != 3:
    raise ValueError("Wrong number of arguments, need exactly two filenames.")

if not pathlib.Path(sys.argv[1]).is_file():
    raise ValueError("Input file does not exist.")

with open(sys.argv[1], 'r') as file:
    opts, freq, data, comment = parse_file(file)

with open(sys.argv[2], 'w+') as file:
    opts_ma = opts.copy()
    opts_ma.update({'format': 'MA'})
    write_file(file, opts_ma, freq, data, comment)
