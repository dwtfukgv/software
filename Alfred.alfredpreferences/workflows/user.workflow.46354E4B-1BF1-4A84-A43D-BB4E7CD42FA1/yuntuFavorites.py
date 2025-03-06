#!/usr/bin/python
# encoding: utf-8
import sys

import utils
import yuntuAction
from utils import get_args, wf


def key_for_record(record):
    return "{} {}".format(
        record[yuntuAction.DASHBOARD_NAME], record[yuntuAction.DASHBOARD_CREATOR]
    )


def main(workflow):
    query, mis, cache_seconds = get_args()
    records = yuntuAction.query_all_favorite_dashboards()
    records = wf().filter(query, records, key_for_record)
    if records:
        for record in records:
            wf().add_item(
                record[yuntuAction.DASHBOARD_NAME],
                "{} - {}".format(
                    record[yuntuAction.DASHBOARD_CREATOR],
                    utils.from_unix_timestamp_HHMM(
                        record[yuntuAction.DASHBOARD_CREATE_TIME] / 1000
                    ),
                ),
                record[yuntuAction.DASHBOARD_KEY],
                valid=True,
            )
    else:
        wf().add_item("no result")
    wf().send_feedback()


if __name__ == "__main__":
    # print(query_all_records())
    sys.exit(wf().run(main))
