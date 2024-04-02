#!/usr/bin/env python3

from touchstone_parser import *
from touchstone_writer import *

with open('./test/LPF.s2p', 'r') as file:
    opts, freq, data, comment = parse_file(file)

with open('./test/generated_LPF.s2p', 'w') as file:
    write_file(file, opts, freq, data, comment)
with open('./test/generated_LPF_MA.s2p', 'w') as file:
    opts_ma = opts.copy()
    opts_ma.update({'format': 'MA'})
    write_file(file, opts_ma, freq, data, comment)
