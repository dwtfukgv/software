#!/usr/bin/python
# encoding: utf-8
import sys

import oceanusAction
from utils import get_args, wf


def key_for_record(record):
    return "{} {}".format(
        record[oceanusAction.NAME], " ".join(record[oceanusAction.APPKEY])
    )


def main(workflow):
    query, mis, cache_seconds = get_args()
    records = wf().cached_data(
        "my_oceanus_sites", oceanusAction.query_all_sites, max_age=int(cache_seconds)
    )
    records = wf().filter(query, records, key_for_record, min_score=10)
    if records:
        for record in records:
            it = wf().add_item(
                record[oceanusAction.NAME],
                ",".join(record[oceanusAction.APPKEY]),
                record[oceanusAction.ID],
                valid=True,
            )
            it.setvar("site_name", record[oceanusAction.NAME])
    else:
        wf().add_item("no result", valid=False)
    wf().send_feedback()


if __name__ == "__main__":
    # print(query_all_records())
    sys.exit(wf().run(main))
