# Word Counter

This is a python 3
(3.5 is recommended)
script that counts alphanumeric
(either Unicode or ASCII, depending on command-line flags)
sequences in a set of files
and reports on the most-frequently-occurring.


## Prerequisites

You must install some python modules to use this program. You can do so via
`pip install -r requirements.txt`


## Running the Program

```
usage: wordcounter.py [-h] [--encoding [ENCODING]] [--limit [LIMIT]]
                      [--ascii-only] [--nodes NODES]
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
  --nodes NODES         comma-separated list of addresses (with optional
                        ports) on which computations may be run. the host must
                        be running a dispynode server. If no port is given, the
                        default (51348) is assumed. Example:
                        0.0.0.0:9999,127.0.0.5
```


### Distributed Operation

Computation can be distributed via 
[dispy](http://dispy.sourceforge.net/),
which handles distribution of code and files to nodes running
[dispynode](http://dispy.sourceforge.net/dispynode.html).

To install the dispy server, simply run
`pip install -r dispy-server-requirements.txt`.

To start the server on <port>, run
`dispynode.py -i 0.0.0.0 --debug --daemon -p <port>`.

You should then be able to pass the hostname or IP address, along with the port,
to the wordcounter using `--nodes`.


## Running Tests

Tests are written with
[unittest](https://docs.python.org/3/library/unittest.html).

You can run:
* individual tests can be run (e.g.,
`python3 -m unittest test.test_counter.WordCounterTest.test_nonempty`),
* all tests in a single script (e.g.,
`python3 -m unittest test.test_counter)`,
* the whole suite via
`python3 -m unittest discover test`.

