"""Tools for extracting words from a stream."""

import re


_ASCII_PATTERN = re.compile('[a-zA-Z0-9]+')


def is_ascii_alnum(s):
    """Does the given string contain only ASCII alphanumeric characters?

    :param s: a string
    :return: True iff the word contains only ASCII alphanumeric characters.
    """
    return _ASCII_PATTERN.match(s)


class WordTokenizer:
    """An iterator over words drawn from a stream."""

    def __init__(self, stream, word_test=str.isalnum):
        """Create an instance.

        :param stream: an io.TextIO object or similar. Must have a read method
         taking an int and returning a string.
        :param word_test: function taking a string and returning True iff
         the string contains only word characters. Default is str.isalnum.
        """
        self._stream = stream
        self._is_string = isinstance(stream, str)
        self._word_test = word_test

    def _chars(self):
        while True:
            # Here we're assuming the stream is buffered for reasonable
            # performance. It would be easy enough to wrap this in another loop
            # over chars with a larger buffer size were it necessary.
            chars = self._stream.read(1)
            if chars == '':
                return
            yield chars

    def _words(self):
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
        # we're out of characters, but we may have accumulated a word that still
        # needs to be returned.
        if word:
            yield word

    def __iter__(self):
        return self._words()
