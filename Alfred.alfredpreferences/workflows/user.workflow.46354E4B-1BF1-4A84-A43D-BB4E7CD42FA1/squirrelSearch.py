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
    query, mis, cache_seconds = get_args()
    squirrel_cluster_list = squirrelAction.query_resource(query)
    if squirrel_cluster_list:
        for cluster in squirrel_cluster_list:
            wf().add_item(
                cluster["resourceName"],
                "[总:{}G 已用:{}%] - [拓扑:{}] - {}".format(
                    cluster["resourceMemSize"],
                    cluster["resourceMemUseRate"] * 100,
                    cluster["resourceTopology"],
                    cluster["description"],
                ),
                cluster["resourceName"],
                valid=True,
            ),

    else:
        wf().add_item("no result")
    workflow.send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
