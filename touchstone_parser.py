#!/usr/bin/env python3
import re
import math
import cmath

whitespace = re.compile(r'\s+', re.I | re.A)
optionsyntax = re.compile(r'(?<=\s|#)(?:(?:([kMG]?Hz))|(?:([SYZGH]))|(?:(DB|MA|RI))|(?:R\s+([\d\.]+)))(?=\s|$)', re.I | re.A)

def parse_options(line):
    defaultOptions = {'freq': 'GHz', 'param': 'S', 'format': 'MA', 'Z0': 50.0}
    freq_casecorr = {'GHZ': 'GHz', 'MHZ': 'MHz', 'KHZ': 'kHz', 'HZ': 'Hz'}
    options = defaultOptions.copy()
    matches = optionsyntax.findall(line)
    for m in matches:
        if m != None and len(m) == 4:
            if m[0] != None and m[0] != '':
                corr = freq_casecorr.get(m[0].upper())
                options.update({'freq': corr})
            if m[1] != None and m[1] != '':
                options.update({'param': m[1].upper()})
            if m[2] != None and m[2] != '':
                options.update({'format': m[2].upper()})
            if m[3] != None and m[3] != '':
                Z0 = float(m[3])
                options.update({'Z0': Z0})
    return options

# Returns (freq, [c1, c2, c3...], comment)
# Where freq is a float, cX is a complex number, comment is a string, may be None.
def parse_data(line, options):
    freq_scaling = {'GHz': 1e9, 'MHz': 1e6, 'kHz': 1e3, 'Hz': 1}
    commentsplit = line.split('!')
    split = whitespace.split(commentsplit[0].strip())
    freq = float(split[0])
    cX = []
    for i in range(1, len(split)-1, 2):
        x1, x2 = float(split[i]), float(split[i+1])
        if options['format'] == 'DB':
            # Decibel-angle format
            cX.append(cmath.rect(math.pow(10, x1/20), math.radians(x2)))
        elif options['format'] == 'RI':
            # Real-imaginary format
            cX.append(x1+1j*x2)
        elif options['format'] == 'MA':
            # Magnitude-angle format.
            cX.append(cmath.rect(x1, math.radians(x2)))
        else:
            raise ValueError("options['format'] must be one of DB, RI, MA.")
    # The comment, if it exists.
    comment = None
    if len(commentsplit) > 1:
        comment = commentsplit[1]
    return (freq*freq_scaling.get(options['freq']), cX, comment)


# returns (code, data)
# (0, None) means comment/ignored double options line
# (1, opts) means options
# (2, data) means data line
def parse_line(line, options):
    if line[0] == '!':
        # Comment line.
        return (0, None)
    elif line[0] == '#':
        # Check: do we have options yet?
        if options == None:
            return (1, parse_options(line))
        # Ignore any subsequent options lines.
        return (0, None)
    elif line.isspace():
        # Blank line, ignore.
        return (0, None)
    else:
        # Data line
        return (2, parse_data(line, options))

def parse_file(file):
    options = None
    freq = []
    vals = []
    comments = []
    for line in file:
        code, data = parse_line(line, options)
        if code == 1:
            options = data
        elif code == 2:
            freq.append(data[0])
            vals.append(data[1])
            comments.append(data[2])
    return (options, freq, vals, comments)
