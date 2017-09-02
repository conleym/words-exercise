import io

import wordcounter
from wordcounter import word_tokenizer


def merge_counts(totals, new_counts):
    for k, v in new_counts.items():
        totals[k] = totals.get(k, 0) + v


def count_words(streams_or_paths, encoding, ascii_only):
    totals = {}
    counter = WordCounter(encoding, ascii_only)
    for stream_or_path in streams_or_paths:
        merge_counts(totals, counter.count_words(stream_or_path))
    return totals


def update_counts(word_counts, current_word):
    current_word_count = word_counts.get(current_word, 0)
    word_counts[current_word] = current_word_count + 1


class WordCounter:
    """Counts the words in a single file."""
    def __init__(self, encoding=wordcounter.DEFAULT_ENCODING,
                 ascii_only=wordcounter.DEFAULT_ASCII_ONLY):
        self._ascii_only = ascii_only
        self._encoding = encoding

    def _words(self, stream):
        if self._ascii_only:
            return word_tokenizer.WordTokenizer(stream,
                                                word_tokenizer.is_ascii_alnum)
        return word_tokenizer.WordTokenizer(stream)

    def count_words(self, stream_or_path):
        if isinstance(stream_or_path, str):
            stream = io.open(stream_or_path, encoding=self._encoding)
        else:
            stream = stream_or_path
        word_counts = {}
        with stream:
            words = self._words(stream)
            for word in words:
                update_counts(word_counts, word.lower())
        return word_counts
