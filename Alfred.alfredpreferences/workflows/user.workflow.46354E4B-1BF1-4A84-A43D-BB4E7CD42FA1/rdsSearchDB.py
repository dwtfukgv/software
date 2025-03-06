#!/usr/bin/python
# encoding: utf-8
import sys

import rdsAction
from utils import get_args, wf


def main(workflow):
    query, mis, cache_seconds = get_args()
    records = rdsAction.query_paged_database(keyword=query)
    if records:
        for record in records:
            it = wf().add_item(
                record[rdsAction.DATABASE_NAME],
                record[rdsAction.DESC],
                record[rdsAction.DATABASE_ID],
                valid=True,
            )
            it.setvar("cluster_id", record[rdsAction.CLUSTER_ID])
    else:
        wf().add_item("no result")
    wf().send_feedback()


if __name__ == "__main__":
    # print(query_all_records())
    sys.exit(wf().run(main))
