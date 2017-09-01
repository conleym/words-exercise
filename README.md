# Word Counter

This is a python 3
(3.6 is recommended)
script that counts alphanumeric
(either Unicode or ASCII, depending on command-line flags)
sequences in a set of files
and reports on the most-frequently-occurring.


## Running the Program

```
usage: wordcounter.py [-h] [--encoding [ENCODING]] [--limit [LIMIT]]
                      [--ascii-only]
                      FILE [FILE ...]

Find the most common words in a corpus of files.

positional arguments:
  FILE                  a file from which words will be read

optional arguments:
  -h, --help            show this help message and exit
  --encoding [ENCODING]
                        encoding of the given files
  --limit [LIMIT]       number of results to return
  --ascii-only          count only ASCII alphanumeric character sequences as
                        words
```

## Running Tests

Test are written with
[unittest](https://docs.python.org/3/library/unittest.html).

You can run:
* individual tests can be run (e.g.,
`python3 -m unittest test.test_counter.WordCounterTest.test_nonempty`),
* all tests in a single script (e.g.,
`python3 -m unittest test.test_counter)`,
* the whole suite via
`python3 -m unittest discover test`.

