#!/usr/bin/python
# encoding: utf-8
import sys

import rdsAction
from utils import get_args, wf


def key_for_record(record):
    return "{} {}".format(record[rdsAction.NAME], record[rdsAction.DESC])


def main(workflow):
    query, mis, cache_seconds = get_args()
    records = wf().cached_data(
        "my_rds_cluster", rdsAction.query_all_clusters, max_age=int(cache_seconds)
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
                record[rdsAction.APPKEY],
                valid=True,
            )
    else:
        wf().add_item("no result", valid=False)
    wf().send_feedback()


if __name__ == "__main__":
    # print(query_all_records())
    sys.exit(wf().run(main))
