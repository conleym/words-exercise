import io

from wordcounter import tokenizer


def _update_count(word_count, current_word):
    current_word_count = word_count.get(current_word, 0)
    word_count[current_word] = current_word_count + 1


def count_file_words(file, encoding):
    word_count = {}
    with io.open(file, encoding=encoding) as stream:
        words = tokenizer.WordTokenizer(stream)
        for word in words:
            _update_count(word_count, word.lower())
    return word_count


def _merge_counts(totals, new_counts):
    for k,v in new_counts.items():
        totals[k] = totals.get(k, 0) + v


def count_words(files, encoding):
    totals = {}
    for file in files:
        _merge_counts(totals, count_file_words(file, encoding))
    return totals
