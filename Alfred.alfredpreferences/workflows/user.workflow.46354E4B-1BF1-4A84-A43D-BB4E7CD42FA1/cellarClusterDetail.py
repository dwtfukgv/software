#!/usr/bin/env python
# encoding: utf-8
import sys

import cellarAction

from utils import wf, get_args


def key_for_record(record):
    return "{} {} {} {} {}".format(
        record[cellarAction.ID],
        record[cellarAction.GROUP_NAME],
        record[cellarAction.GROUP_DESC],
        record[cellarAction.CELL],
        record[cellarAction.ROLE],
    )


def main(workflow):
    import os

    remote_appkey = os.getenv("remoteappkey")
    query, mis, cache_seconds = get_args()
    cellar_dict = workflow.cached_data(
        "cellar_list_cache",
        lambda: cellarAction.query_all_clusters(10),
        max_age=int(cache_seconds),
    )
    records = []
    if remote_appkey:
        records = cellar_dict[remote_appkey]
    else:
        if cellar_dict:
            for k, v in cellar_dict.items():
                records.extend(v)
    records = wf().filter(query, records, key_for_record)
    if records:
        for record in records:
            wf().add_item(
                "[{}]{}".format(
                    record[cellarAction.ROLE], record[cellarAction.GROUP_NAME]
                ),
                "[{}]{}".format(
                    record[cellarAction.CELL], record[cellarAction.GROUP_DESC]
                ),
                record[cellarAction.ID],
                valid=True,
            )
    else:
        wf().add_item("no result")
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
