#!/usr/bin/env python
# encoding: utf-8
import sys

import squirrelAction

from utils import wf, get_args


def key_for_record(record):
    return "{} {} {} {}".format(
        record[squirrelAction.CLUSTER_NAME],
        record[squirrelAction.TOPOLOGY],
        record[squirrelAction.TOTAL_MEM],
        record[squirrelAction.USED_MEM],
    )


def main(workflow):
    import os

    group_name = os.getenv("group_name")
    query, mis, cache_seconds = get_args()
    squirrel_cluster_list = workflow.cached_data(
        "squirrel_list_cache",
        lambda: squirrelAction.query_all_clusters(10),
        max_age=int(cache_seconds),
    )
    if group_name:
        pass
        # records = squirrel_cluster_list[remote_appkey]

    squirrel_cluster_list = wf().filter(query, squirrel_cluster_list, key_for_record)
    if squirrel_cluster_list:
        for record in squirrel_cluster_list:
            wf().add_item(
                record[squirrelAction.CLUSTER_NAME],
                "[容量:{}/{}G] - [拓扑:{}] - [DBA:{}]".format(
                    record[squirrelAction.USED_MEM],
                    record[squirrelAction.TOTAL_MEM],
                    record[squirrelAction.TOPOLOGY],
                    record[squirrelAction.DBA_ALIAS],
                ),
                record[squirrelAction.CLUSTER_NAME],
                valid=True,
            )
    else:
        wf().add_item(query, "", query, valid=True)
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
