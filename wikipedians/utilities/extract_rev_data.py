#!/usr/bin/env python
"""Extracts times, namespaces and user names of all revisions in a dump.

Usage:
    extract_rev_data <dump-file>... [--threads=<num>] [--output=<path>]
                                    [--verbose] [--debug]
    extract_rev_data -h | --help

Options:
    -h --help           Show this screen.
    <dump-file>         An XML dump file to process
    --threads=<num>     If a collection of files are provided, how many
                        processor threads should be prepare?
                        [default: <cpu_count>]
    --output=<path>     The path to a file to dump observations to
                        [default: <stdout>]
    --verbose           Prints page names to <stderr>
    --debug             Print debug level logging
"""
import docopt
import json
import logging
import mwxml
import os.path
import sys
from multiprocessing import cpu_count


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)

    dump_paths = args['<dump-file>']

    if args['--threads'] == "<cpu_count>":
        threads = cpu_count()
    else:
        threads = int(args['--threads'])

    if args['--output'] == "<stdout>":
        output = sys.stdout
    else:
        output = open(os.path.expanduser(args['--output']), "w")

    verbose = args['--verbose']
    debug = args['--debug']

    logging.basicConfig(
        level=logging.DEBUG if debug else logging.WARNING,
        format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
    )

    run(dump_paths, threads, output, verbose=verbose)


def run(dump_paths, threads, output, verbose=False):

    if len(dump_paths) == 0:
        user_edits = extract_rev_data(mwxml.Dump.from_file(sys.stdin),
                                      verbose=verbose)

    else:
        user_edits = mwxml.map(lambda d, p:
                               extract_rev_data(d, verbose),
                               dump_paths, threads=threads)

    for edit in user_edits:
        json.dump(edit, output)
        output.write("\n")


def extract_rev_data(dump, verbose=False):
    """
    Extracts unix time, namespace and user of revisions from
    :class:`mwxml.Dump`.

    :Parameters:
        dump : :class:`mwxml.Dump`
            The XML dump file to extract labelings from
        verbose : `bool`
            Print page names to stderr

    :Returns:
        An iterator of dicts containing:

        * t -- The unix time of the revision
        * n -- The namespace of the edited page
        * u -- The user who made the revision
    """

    for page in dump:
        if verbose:
            sys.stderr.write("\n{0}".format(page.title))
            sys.stderr.flush()
        for rev in page:
            yield {'t': rev.timestamp.unix(), 'n': page.namespace,
                   'u': (rev.user.text if rev.user is not None else '')}


if __name__ == '__main__':
    main()
