"""Iterate over words in a stream."""

import re
from typing import Callable, Generator, IO, Iterable


_ASCII_PATTERN = re.compile('[a-zA-Z0-9]+')


def is_ascii_alnum(s: str) -> bool:
    """Does the given string contain only ASCII alphanumeric characters?

    :param s: a string
    :return: True iff the word contains only ASCII alphanumeric characters.
    """
    return _ASCII_PATTERN.match(s) is not None


class WordTokenizer(Iterable):
    """An iterator over words drawn from a stream."""

    def __init__(self, stream: IO[str],
                 word_test: Callable[[str], bool]=str.isalnum) -> None:
        """Create an instance.

        :param stream: The stream to tokenize. For performance reasons, this
         stream should be buffered.
        :param word_test: A callable taking a string and returning True iff
         the string contains only word characters. Default is str.isalnum.
        """
        self._stream = stream
        self._word_test = word_test

    def _chars(self) -> Generator[str, None, None]:
        while True:
            # Here we're assuming the stream is buffered for reasonable
            # performance. It would be easy enough to wrap this in another loop
            # over chars with a larger buffer size were it necessary.
            chars = self._stream.read(1)
            if chars == '':  # EOF
                return
            yield chars

    def __iter__(self) -> Generator[str, None, None]:
        word = ''
        for char in self._chars():
            if self._word_test(char):
                word += char
            # word boundary reached:
            # if we've already accumulated a word, return it.
            # otherwise, we've seen nothing but whitespace, so we need to
            # continue trying to accumulate a word.
            elif word:
                yield word
                word = ''
        # we're out of characters, but we may have accumulated a word that
        # still needs to be returned.
        if word:
            yield word
