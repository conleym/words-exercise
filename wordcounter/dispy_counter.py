"""Count words in a series of files using distributed computation."""

from typing import Callable, Dict, Iterable, no_type_check

import dispy
from dispy import NodeAllocate

from wordcounter import word_counter
from wordcounter.word_counter import WordCounter


_DispyCallbackType = Callable[[int, dispy.DispyNode, dispy.DispyJob], None]


# Don't use type annotations here -- not sure how to send them to nodes.
# Also don't use decorators. They seem not to go, either :(
def _computation(path, counter):
    """Computation to distribute to the nodes."""
    return counter.count_words(path)


def _dispy_create_cluster(status_cb: _DispyCallbackType,
                          nodes: Iterable[NodeAllocate]) -> dispy.JobCluster:
    """Create a dispy job cluster to run word counting jobs."""
    import wordcounter

    # Code required by the computation. Will be sent to each node.
    dependencies = [wordcounter, wordcounter.word_tokenizer,
                    wordcounter.word_counter]
    return dispy.JobCluster(_computation, nodes=nodes, ip_addr="127.0.0.1",
                            cluster_status=status_cb, depends=dependencies,
                            reentrant=True)


def dispy_count_words(paths: Iterable[str],
                      counter: WordCounter,
                      nodes: Iterable[NodeAllocate]) -> Dict[str, int]:
    """Count words in one or more files and return total counts.

    The computation is distributed to a dispy cluster consisting of the given
    nodes, which must be running the dispynode.py server. dispy will send
    both the code needed to perform computation and the files to each node as
    needed.

    :param paths: The input sources.
    :param counter: The WordCounter to use.
    :param nodes: The dispy nodes to which computation should be distributed.
    :return: A dict mapping each word found to the number of times it was found
     in all the input sources.
    """
    totals = {}  # type: Dict[str, int]

    # dispy will complain if we try to annotate this. It's ok w/ decorators,
    # though.
    @no_type_check
    def status_cb(status, _node, _job):
        if status == dispy.DispyJob.Finished:
            word_counter.merge_counts(totals, _job.result)
        elif status == dispy.DispyJob.Terminated:
            print("Error counting words in %s on node %s: %s" %
                  (_job.id, _node, _job.exception))

    with _dispy_create_cluster(status_cb, nodes) as cluster:
        cluster.print_status()
        for path in paths:
            job = cluster.submit(path, counter,  # args to computation
                                 # sends file to node
                                 dispy_job_depends=[path])
            job.id = path
        cluster.wait()
        cluster.print_status()
    return totals
