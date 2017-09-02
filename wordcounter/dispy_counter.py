import dispy
from wordcounter import word_counter


def dispy_create_cluster(computation, status_cb, nodes, wc):
    import wordcounter
    dependencies = [wordcounter, word_counter]
    return dispy.JobCluster(computation, nodes=nodes, ip_addr="0.0.0.0",
                            cluster_status=status_cb, depends=dependencies,
                            reentrant=True)


def dispy_count_words(paths, encoding, ascii_only, nodes):
    node_names = [node[0] for node in nodes]
    wc = word_counter.WordCounter(encoding, ascii_only)
    totals = {}

    def status_cb(status, _node, _job):
        if status == dispy.DispyJob.Finished:
            print(_job.result)
            word_counter.update_count(totals, _job.result)
        elif status == dispy.DispyJob.Terminated:
            print("Error counting words in %s on node %s: %s" %
                  (job.id, _node, job.exception))
        else:
            print("Got job status %s" % status)

    def computation(_path):
        print("Counting words for %s" % _path)
        # word_counts = wc.count_words(_path)
        # print("Counted %s words for %s" % word_counts, _path)
        # return word_counts
        return {}

    def random_node():
        import random

        return random.choice(node_names)

    cluster = dispy_create_cluster(computation, status_cb, nodes, word_counter)
    for path in paths:
        path_node = random_node()
        print("Sending %s to %s" % (path, path_node))
        cluster.send_file(path, path_node)
        job = cluster.submit_node(path_node, path)
        if job is not None:
            job.id = path
    cluster.wait()
    cluster.print_status()
    return totals