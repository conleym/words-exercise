#! /usr/bin/env python3

import argparse
import wordcounter


def _invert_counts(counts):
    inverted = {}
    for k, v in counts.items():
        words_for_count = inverted.get(v, [])
        words_for_count.append(k)
        inverted[v] = words_for_count
    return inverted


def top_words(streams, encoding, n, ascii_only, nodes):
    from wordcounter import word_counter, dispy_counter

    if nodes:
        counts = dispy_counter.dispy_count_words(streams, encoding, ascii_only,
                                                 nodes)
    else:
        counts = word_counter.count_words(streams, encoding, ascii_only)
    inverted = _invert_counts(counts)
    sorted_counts = sorted(inverted.items(), key=lambda x: x[0], reverse=True)
    return sorted_counts[:n]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Find the most common words in a corpus of files.')
    parser.add_argument('files', nargs='+', metavar='FILE',
                        help='a file from which words will be read')
    parser.add_argument('--encoding', nargs='?',
                        help='encoding of the given files',
                        default=wordcounter.DEFAULT_ENCODING)
    parser.add_argument('--limit', nargs='?',
                        help='number of results to return', type=int,
                        default=10)
    parser.add_argument('--ascii-only',
                        help='count only ASCII alphanumeric character sequences'
                             ' as words', action='store_true',
                        default=wordcounter.DEFAULT_ASCII_ONLY)
    parser.add_argument('--nodes',
                        help='comma-separated list of addresses (with optional'
                             ' ports) on which computations may be run. the'
                             ' host must be running a dispynode server. If no'
                             ' port is given, the default (51348) is assumed.'
                             ' Example: 0.0.0.0:9999,127.0.0.5',
                        default=None)
    parsed_args = parser.parse_args()
    arg_nodes = None
    if parsed_args.nodes is not None:
        arg_nodes = [node.split(':') for node in parsed_args.nodes.split(',')]

    file_args = frozenset(parsed_args.files)  # remove duplicates
    print(top_words(file_args, parsed_args.encoding, parsed_args.limit,
                    parsed_args.ascii_only, arg_nodes))
