"""Count words in a group of files or streams."""

import io
from typing import Dict, IO, Iterable

from wordcounter import (DEFAULT_ASCII_ONLY, DEFAULT_ENCODING, StreamOrPath,
                         word_tokenizer)


def merge_counts(totals: Dict[str, int], new_counts: Dict[str, int]) -> None:
    """Merge counts from a source into a running total over several sources."""
    for k, v in new_counts.items():
        totals[k] = totals.get(k, 0) + v


class WordCounter:
    """Counts the words in a body of text."""

    def __init__(self, encoding: str=DEFAULT_ENCODING,
                 ascii_only: bool=DEFAULT_ASCII_ONLY) -> None:
        """Create an instance.

        :param encoding: The text encoding to use when opening files. Unused
         for streams.
        :param ascii_only: If True, count only ASCII alphanumeric character
         sequences as words. Otherwise, count Unicode alphanumeric sequences as
         words.
        """
        self._ascii_only = ascii_only
        self._encoding = encoding

    def _words(self, stream: IO[str]) -> word_tokenizer.WordTokenizer:
        if self._ascii_only:
            return word_tokenizer.WordTokenizer(stream,
                                                word_tokenizer.is_ascii_alnum)
        return word_tokenizer.WordTokenizer(stream)

    def count_words(self, stream_or_path: StreamOrPath) -> Dict[str, int]:
        """Count words in the given input source.

        :param stream_or_path: the input source.
        :return: a dict mapping each word found to the number of times it was
         found in the input source.
        """
        if isinstance(stream_or_path, str):
            stream = io.open(stream_or_path, encoding=self._encoding)
        else:
            stream = stream_or_path
        word_counts = {}  # type: Dict[str, int]
        with stream:
            words = self._words(stream)
            for word in words:
                # Count is case-insensitive. Arbitrarily convert to lowercase.
                word = word.lower()
                word_counts[word] = word_counts.get(word, 0) + 1
        return word_counts


def count_words(streams_or_paths: Iterable[StreamOrPath],
                counter: WordCounter) -> Dict[str, int]:
    """Count words in one or more input sources and return total counts.

    :param streams_or_paths: The input sources.
    :param counter: The WordCounter to use.
    :return: A dict mapping each word found to the number of times it was found
     in all the input sources.
    """
    totals = {}  # type: Dict[str, int]
    for stream_or_path in streams_or_paths:
        merge_counts(totals, counter.count_words(stream_or_path))
    return totals
