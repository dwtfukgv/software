#!/usr/bin/env python
# encoding: utf-8
import os
import sys

import squirrelAction

from utils import wf, get_args


def key_for_record(record):
    return "{} {}".format(record[squirrelAction.CLUSTER_NAME], record["unitName"])


def main(workflow):
    query, mis, cache_seconds = get_args()
    group_name = os.getenv("group_name")
    squirrel_cluster_list = squirrelAction.query_all_cluster_of_group(group_name)
    wf().logger.log(level=20, msg=squirrel_cluster_list)
    squirrel_cluster_list = wf().filter(query, squirrel_cluster_list, key_for_record)
    if squirrel_cluster_list:
        for record in squirrel_cluster_list:
            wf().add_item(
                record[squirrelAction.CLUSTER_NAME],
                "[{}]".format(record["unitName"]),
                record[squirrelAction.CLUSTER_NAME],
                valid=True,
            )
    else:
        wf().add_item("no result")
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
