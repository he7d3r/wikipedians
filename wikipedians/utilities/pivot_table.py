#!/usr/bin/env python
"""Create pivot table of the revision data and output a CSV file.

Usage:
    pivot_table.py [--input=<path>] [--output=<path>] [--verbose]
    pivot_table.py -h | --help

Options:
    -h --help           Show this screen.
    --input=<path>      The path of a CSV file with a revision per row, as in
                        e.g.:
                            timestamp user edits
                            2000-01   Me   123
                            2000-02   Me   321
                            2000-01   John 222
                        [default: <stdin>]
    --output=<path>     The path to a file to save a pivot table such as
                            user 2000-01 2000-02
                            John 222.0
                            Me   123.0   321.0
                        [default: <stdout>]
    --verbose           Prints dots to <stderr>
"""
import docopt
import sys
import os.path
import pandas as pd


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)
    if args['--input'] == "<stdin>":
        input = sys.stdin
    else:
        input = open(args['--input'])

    if args['--output'] == "<stdout>":
        output = sys.stdout
    else:
        output = open(os.path.expanduser(args['--output']), "w")

    verbose = args['--verbose']
    pivot_table(input, output, verbose=verbose)


def pivot_table(input, output, verbose):
    if verbose:
        sys.stderr.write('Creating pivot table\n')
        sys.stderr.flush()
    df = pd.read_csv(input)
    pivot_table = pd.pivot_table(df, index='user', values='edits',
                                 columns=set(df.columns) - {'user', 'edits'})
    pivot_table.to_csv(output)


if __name__ == '__main__':
    main()
