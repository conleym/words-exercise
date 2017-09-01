import unittest
from wordcounter import counter


_TEST_WORDS = """
    a test. a word. word word word.

    A TEST.
"""

_EXPECTED_COUNTS = {
    'a': 3,
    'test': 2,
    'word': 4
}


class WordCounterTest(unittest.TestCase):
    def test_counter(self):
        import io

        wc = counter.WordCounter()
        counts = wc.count_words(io.StringIO(_TEST_WORDS))
        self.assertEqual(_EXPECTED_COUNTS, counts)


if __name__ == '__main__':
    unittest.main()
