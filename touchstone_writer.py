#!/usr/bin/env python3
import math
import cmath

def format_data_line(options, freq, fscale, channels, comment):
    builder = "{}".format(freq/fscale)
    for value in channels:
        builder += data_to_string(options, value)
    if comment != None:
        builder += ' !{}'.format(comment)
    builder += '\n'
    return builder

def data_to_string(options, n):
    if options['format'] == 'MA':
        mag = abs(n)
        phase = math.degrees(cmath.phase(n))
        return " {} {}".format(mag, phase)
    elif options['format'] == 'RI':
        return " {} {}".format(n.real, n.imag)
    elif options['format'] == 'DB':
        mag_db = 20*math.log10(abs(n))
        phase = math.degrees(cmath.phase(n))
        return " {} {}".format(mag_db, phase)


def write_file(file, options, freq, data, comment):
    freq_casecorr = {'GHZ': 'GHz', 'MHZ': 'MHz', 'KHZ': 'kHz', 'HZ': 'Hz'}
    freq_scaling = {'GHz': 1e9, 'MHz': 1e6, 'kHz': 1e3, 'Hz': 1}
    fscale = freq_scaling.get(freq_casecorr.get(options['freq'].upper()))

    # Write the options line.
    file.write('# {} {} {} R {}\n'.format(options['freq'], options['param'], options['format'], options['Z0']))
    # Confirm that the lengths match.
    assert len(freq) == len(data)
    for i in range(len(freq)):
        line = format_data_line(options, freq[i], fscale, data[i], comment[i])
        file.write(line)
