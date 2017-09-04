#! /usr/bin/env python3

"""Count words in some files and display the most-frequently-occurring."""

import argparse
from typing import Dict, Iterable

from dispy import NodeAllocate

from wordcounter import (DEFAULT_ASCII_ONLY, DEFAULT_ENCODING, StreamOrPath)


# Dict of counts -> list of words counted that many times.
ResultType = Dict[int, Iterable[str]]


def _invert_counts(counts: Dict[str, int]) -> ResultType:
    inverted = {}
    for k, v in counts.items():
        words_for_count = inverted.get(v, [])
        words_for_count.append(k)
        inverted[v] = words_for_count
    return inverted


def top_words(streams_or_paths: Iterable[StreamOrPath],
              encoding: str,
              n: int,
              ascii_only: bool,
              nodes: Iterable[NodeAllocate]) -> ResultType:
    from wordcounter import word_counter, dispy_counter

    counter = word_counter.WordCounter(encoding, ascii_only)
    if nodes:
        counts = dispy_counter.dispy_count_words(streams_or_paths, counter,
                                                 nodes)
    else:
        counts = word_counter.count_words(streams_or_paths, counter)
    inverted = _invert_counts(counts)
    sorted_counts = sorted(inverted.items(), key=lambda x: x[0], reverse=True)
    return sorted_counts[:n]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__)
    parser.add_argument('files', nargs='+', metavar='FILE',
                        help='a file from which words will be read')
    parser.add_argument('--encoding', nargs='?',
                        help='encoding of the given files',
                        default=DEFAULT_ENCODING)
    parser.add_argument('--limit', nargs='?',
                        help='number of results to return', type=int,
                        default=10)
    parser.add_argument('--ascii-only',
                        help='count only ASCII alphanumeric character '
                             ' sequences as words', action='store_true',
                        default=DEFAULT_ASCII_ONLY)
    parser.add_argument('--nodes',
                        help='comma-separated list of addresses (with optional'
                             ' ports) on which computations may be run. the'
                             ' host must be running a dispynode server. If no'
                             ' port is given, the default (51348) is assumed.'
                             ' Example: 0.0.0.0:9999,127.0.0.5',
                        default=None)
    parsed_args = parser.parse_args()
    arg_nodes = []
    if parsed_args.nodes is not None:
        arg_nodes = [node.split(':') for node in parsed_args.nodes.split(',')]
        # This makes type checking _much_ easier.
        arg_nodes = [NodeAllocate(*node) for node in arg_nodes]

    file_args = frozenset(parsed_args.files)  # remove duplicates

    # The output format, admittedly, is not ideal in many cases.
    print(top_words(file_args, parsed_args.encoding, parsed_args.limit,
                    parsed_args.ascii_only, arg_nodes))
