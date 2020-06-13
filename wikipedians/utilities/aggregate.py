#!/usr/bin/env python
"""Aggregates the number of edits by users by day (or month) and outputs a CSV
file.

Usage:
    aggregate.py [--input=<path>] [--output=<path>] [--min-edits=<int>]
                 [--monthly] [--verbose]
    aggregate.py -h | --help

Options:
    -h --help           Show this screen.
    --input=<path>      The path of a file with a JSON per row, whose keys are
                        * t -- The unix time of the revision
                        * n -- The namespace of the edited page
                        * u -- The user who made the revision
                        E.g.:
                            {"n": 0, "t": 123456789, "u": "John"}
                        [default: <stdin>]
    --output=<path>     The path to a file to save the aggregate data
                        [default: <stdout>]
    --min-edits=<int>   The minimum number of edits a user must have to be
                        included in the output [default: 5]
    --monthly           Group by month instead of day
    --verbose           Prints dots to <stderr>
"""
import docopt
import sys
import os.path
import pandas as pd

from wikipedians.utilities.filter import remove_users_with_few_edits


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
    threshold = int(args['--min-edits'])
    monthly = args['--monthly']
    verbose = args['--verbose']

    run(input, output, threshold, monthly, verbose=verbose)


def run(input, output, threshold, monthly, verbose=False):
    all_chunks = read_and_group_file_in_chunks(input, monthly=monthly,
                                               verbose=verbose)
    frequent_users = remove_users_with_few_edits(all_chunks,
                                                 threshold=threshold,
                                                 verbose=verbose)
    if verbose:
        sys.stderr.write('Aggregating the edit counts from different chunks\n')
        sys.stderr.flush()
    df = frequent_users.groupby(frequent_users.index.names).sum()
    df.to_csv(output)


def read_and_group_file_in_chunks(input, monthly, verbose=False):
    grouped_chunks = []
    size = 1000000
    if verbose:
        sys.stderr.write('Reading file in chunks of {} lines'.format(size))
        sys.stderr.flush()
    for chunk in pd.read_json(input, lines=True, convert_dates='t',
                              chunksize=size):
        if verbose:
            sys.stderr.write('.')
            sys.stderr.flush()
        chunk = chunk.rename(columns={'t': 'timestamp', 'n': 'namespace',
                                      'u': 'user'})
        if monthly:
            period = '%Y-%m'
        else:
            period = '%Y-%m-%d'
        grouped_chunks.append(count_by_period_user_and_ns(chunk, period))

    if verbose:
        sys.stderr.write('\nConcatenating {} chunks\n'.format(
                         len(grouped_chunks)))
        sys.stderr.flush()
    return pd.concat(grouped_chunks)


def count_by_period_user_and_ns(df, period):
    gr_levels = [df.timestamp.dt.strftime(period), df.user, df.namespace]
    return df.groupby(gr_levels)[['timestamp']].count()\
        .rename(columns={'timestamp': 'edits'})


if __name__ == '__main__':
    main()
