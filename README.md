# GNU wc Reverse Engineering

The wc program is a work-alike reimplementation of GNU’s wc tool, written in Python. It takes an arbitrary number of file names and prints newline, word and byte counts for each one, while also displaying the total number of counts (if the input files where more than one). It can also take optional flags, in order to print specific counts (ex. Lines only) or provide a “help” and “version” message. Unit tests abd doctests where used for testing
