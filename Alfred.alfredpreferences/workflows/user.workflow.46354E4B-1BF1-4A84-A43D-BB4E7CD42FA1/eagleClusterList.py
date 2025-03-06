#!/usr/bin/env python
# encoding: utf-8
import sys

from eagleAction import get_all_clusters_by_type, ESCluster
from utils import get_args, wf


def key_for_record(record: ESCluster):
    return f"{record.clusterName} {record.desc} {record.appkey}"


def main(workflow):
    query, mis, cache_seconds = get_args()
    records = wf().cached_data(
        "meituan_eagle_my_clusters",
        lambda : get_all_clusters_by_type("mine"),
        max_age=int(cache_seconds),
    )
    records = wf().filter(query, records, key_for_record)
    if records:
        for record in records:
            wf().add_item(
                record.clusterName,
                f"【等级：{record.sla}-{record.esStatus}】{record.appkey}-{record.desc or ''}",
                arg=record.clusterName,
                valid=True,
            )
    else:
        wf().add_item("no result")
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))