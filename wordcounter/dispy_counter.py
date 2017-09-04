import dispy
from wordcounter import word_counter


def dispy_create_cluster(computation, status_cb, nodes):
    import wordcounter
    dependencies = [wordcounter, wordcounter.word_tokenizer,
                    wordcounter.word_counter]
    return dispy.JobCluster(computation, nodes=nodes, ip_addr="127.0.0.1",
                            cluster_status=status_cb, depends=dependencies,
                            reentrant=True)


def dispy_count_words(paths, counter, nodes):
    totals = {}

    def status_cb(status, _node, _job):
        if status == dispy.DispyJob.Finished:
            word_counter.merge_counts(totals, _job.result)
        elif status == dispy.DispyJob.Terminated:
            print("Error counting words in %s on node %s: %s" %
                  (job.id, _node, job.exception))

    def computation(_path, _wc):
        return _wc.count_words(_path)

    with dispy_create_cluster(computation, status_cb, nodes) as cluster:
        cluster.print_status()
        for path in paths:
            job = cluster.submit(path, counter, dispy_job_depends=[path])
            job.id = path
        cluster.wait()
        cluster.print_status()
    return totals
