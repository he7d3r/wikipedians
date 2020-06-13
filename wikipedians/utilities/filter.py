#!/usr/bin/env python
"""Filter the revisions by namespace and minimum number of edits.

Usage:
    filter.py [--input=<path>] [--output=<path>] [--min-edits=<int>]
                 [--verbose] [--ns=<int>...]
    filter.py -h | --help

Options:
    -h --help           Show this screen.
    --input=<path>      The path of a CSV file with a revision per row
                        E.g.:
                            timestamp user namespace edits
                            2000-01   Me   0         123
                        [default: <stdin>]
    --output=<path>     The path to a file to save the filtered data
                        [default: <stdout>]
    --min-edits=<int>   The minimum number of edits a user must have to be
                        included in the output [default: 1]
    --ns=<int>          The namespace(s) where the edits to be kept were made
                        [default: all]
    --verbose           Prints info to <stderr>
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

    if args['--ns'] == ["all"]:
        namespaces = None
    else:
        namespaces = [int(x) for x in args['--ns']]
    if args['--min-edits'] == "1":
        threshold = None
    else:
        threshold = int(args['--min-edits'])

    verbose = args['--verbose']

    run(input, output, namespaces=namespaces, threshold=threshold,
        verbose=verbose)


def run(input, output, namespaces=None, threshold=None, verbose=False):
    df = pd.read_csv(input)
    if namespaces is not None:
        df = restrict_to_namespaces(df, namespaces=namespaces, verbose=verbose)
    if threshold is not None:
        df = remove_users_with_few_edits(df, threshold=threshold,
                                         verbose=verbose)
    df.to_csv(output, index=False)


def restrict_to_namespaces(df, namespaces=None, verbose=False):
    if namespaces is None:
        return df
    if type(namespaces) != list:
        namespaces = [namespaces]
    if verbose:
        sys.stderr.write('Restricting to edits in namespace(s) {}\n'.format(
                         namespaces))
        sys.stderr.flush()
    # TODO: Allow namespace to be part of a multi level index
    df = df[df.namespace.isin(namespaces)]
    if len(namespaces) == 1:
        df = df.drop('namespace', axis=1)
    return df


def remove_users_with_few_edits(df, threshold=5, verbose=False):
    if verbose:
        sys.stderr.write('Removing users with less than {} edits\n'.format(
                         threshold))
        sys.stderr.flush()
    if 'user' in df.columns:
        user = df.user
    else:
        user = df.index.get_level_values('user')
    user_totals = df.groupby(user)['edits'].sum()
    names_of_frequent_users = user_totals[user_totals >= threshold].index
    frequent_users = df[user.isin(names_of_frequent_users)]
    return frequent_users


if __name__ == '__main__':
    main()
