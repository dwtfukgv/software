#!/usr/bin/python
# encoding: utf-8
import sys

from utils import get_args_with_env, wf, Environment
import rdsAction


def key_for_record(record):
    return "{} {}".format(record[rdsAction.NAME], record[rdsAction.DESC])


def main(workflow):
    query, mis, cache_seconds, env = get_args_with_env()
    records = wf().cached_data(
        "my_rds_cluster_" + env,
        lambda: rdsAction.query_all_clusters(Environment.get_env(env)),
        max_age=int(cache_seconds),
    )
    records = wf().filter(query, records, key_for_record)
    if records:
        for record in records:
            wf().add_item(
                "集群：{}".format(record[rdsAction.NAME]),
                "[{}-{}节点]{} - {}".format(
                    record[rdsAction.LEVEL],
                    record[rdsAction.NODE_NUM],
                    record[rdsAction.DBAUSER],
                    record[rdsAction.DESC],
                ),
                record[rdsAction.ID],
                valid=True,
            )
    else:
        wf().add_item("no result", valid=False)
    wf().send_feedback()


if __name__ == "__main__":
    # print(query_all_records())
    sys.exit(wf().run(main))
