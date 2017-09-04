import unittest
from typing import Dict

from wordcounter import word_counter


_TEST_WORDS = """
    a test. a word. word word word.

    A TEST.
"""

_EXPECTED_COUNTS = {
    'a': 3,
    'test': 2,
    'word': 4
}


def _count_words(words_string: str) -> Dict[str, int]:
    import io

    wc = word_counter.WordCounter()
    return wc.count_words(io.StringIO(words_string))


class WordCounterTest(unittest.TestCase):
    def test_nonempty(self):
        counts = _count_words(_TEST_WORDS)
        self.assertEqual(_EXPECTED_COUNTS, counts)

    def test_empty(self):
        counts = _count_words("")
        self.assertEqual({}, counts)

    def test_wordless(self):
        counts = _count_words("\n\n\t  \t  \n{  ")
        self.assertEqual({}, counts)
