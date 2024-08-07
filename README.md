# audrey
A tool for parsing and writing Touchstone (sNp) files. There is presently no documentation.

The library itself is in `touchstone_parser.py` and `touchstone_writer.py`. `toMA.py` converts a file to magnitude-angle format, `topickle.py` parses the touchstone file and creates a `.pkl` of the data for future use by python programs. `toRI.py` converts to real-imaginary format.

### Name explanation
Touchstone is a jester in Shakespeare's play _As You Like It_. He ends up marrying Audrey, so I thought it fitting that a library intended to be a companion for touchstone files should be called `audrey`.
