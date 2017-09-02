import io
import unittest

from wordcounter import word_tokenizer


_TEST_WORDS = """one
    two \t\t 3xx
    
    été 
     
    more words here"""

_ASCII_WORDS = ["one", "two", "3xx", "t", "more", "words", "here"]
_UNICODE_WORDS = [word if word != 't' else 'été' for word in _ASCII_WORDS]


class TokenizerTest(unittest.TestCase):
    def setUp(self):
        self.stream = io.StringIO(_TEST_WORDS)

    def test_ascii(self):
        words = word_tokenizer.WordTokenizer(self.stream,
                                             word_tokenizer.is_ascii_alnum)
        self.assertEqual(_ASCII_WORDS, list(words))

    def test_unicode(self):
        words = word_tokenizer.WordTokenizer(self.stream)
        self.assertEqual(_UNICODE_WORDS, list(words))


def _unicode_tokenizer(string):
    return word_tokenizer.WordTokenizer(io.StringIO(string))


class EmptyTokenizerTest(unittest.TestCase):
    def test_empty(self):
        words = _unicode_tokenizer("")
        self.assertEqual([], list(words))

    def test_wordless(self):
        words = _unicode_tokenizer("   \t\t\n +   ")
        self.assertEqual([], list(words))
