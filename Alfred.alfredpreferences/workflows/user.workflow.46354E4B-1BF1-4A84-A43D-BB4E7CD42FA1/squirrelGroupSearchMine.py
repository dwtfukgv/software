#!/usr/bin/env python
# encoding: utf-8
import sys

import squirrelAction

from utils import wf, get_args


def key_for_record(record):
    return "{} {} {} {}".format(
        record[squirrelAction.GROUP_NAME],
        record[squirrelAction.APPLICATION_LOCATION],
        record[squirrelAction.GROUP_TYPE],
        record[squirrelAction.GROUP_DESC],
    )


def main(workflow):
    query, mis, cache_seconds = get_args()
    squirrel_cluster_list = workflow.cached_data(
        "squirrel_group_list_cache",
        lambda: squirrelAction.query_all_cluster_groups(10),
        max_age=int(cache_seconds),
    )
    squirrel_cluster_list = wf().filter(query, squirrel_cluster_list, key_for_record)
    if squirrel_cluster_list:
        for record in squirrel_cluster_list:
            wf().add_item(
                record[squirrelAction.GROUP_NAME],
                "[{}][{}] - {}".format(
                    record[squirrelAction.GROUP_TYPE],
                    record[squirrelAction.APPLICATION_LOCATION],
                    record[squirrelAction.GROUP_DESC],
                ),
                record[squirrelAction.GROUP_NAME],
                valid=True,
            )
    else:
        wf().add_item("no result")
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
