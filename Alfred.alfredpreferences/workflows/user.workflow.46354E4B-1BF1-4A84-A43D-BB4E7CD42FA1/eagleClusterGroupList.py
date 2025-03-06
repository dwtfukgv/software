#!/usr/bin/env python
# encoding: utf-8
import sys

from eagleAction import get_all_cluster_groups, get_cluster_groups, ESClusterGroup
from utils import get_args, wf


def key_for_record(record: ESClusterGroup):
    return f"{record.groupName} {record.clusterGroupAppkey}"


def main(workflow):
    query, mis, cache_seconds = get_args()
    records = wf().cached_data(
        "meituan_eagle_my_cluster_groups",
        get_all_cluster_groups,
        # get_cluster_groups,
        max_age=int(cache_seconds),
    )
    records = wf().filter(query, records, key_for_record)
    if records:
        for record in records:
            wf().add_item(
                record.groupName,
                record.clusterGroupAppkey,
                arg=record.groupName,
                valid=True,
            )
    else:
        wf().add_item("no result")
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))