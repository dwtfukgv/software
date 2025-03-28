#!/usr/bin/python
# encoding: utf-8
import sys

import utils
import radarAction
from utils import get_args, wf


def key_for_record(record):
    return "{} {}".format(
        record[radarAction.RADAR_INCIDENT_BRIEF], record[radarAction.RADAR_LEVEL]
    )


def main(workflow):
    query, mis, cache_seconds = get_args()
    import os

    radar_org_id = os.getenv("radar_org_id")
    if not radar_org_id:
        wf().add_item(
            "No Radar Org ID, set radar_org_id to environment variable in alfred"
        )
    else:
        records = radarAction.query_all_event(radar_org_id)
        records = wf().filter(query, records, key_for_record)
        if records:
            for record in records:
                wf().add_item(
                    record[radarAction.RADAR_INCIDENT_BRIEF],
                    "[定级:{}-状态：{}] at {} by {}".format(
                        record[radarAction.RADAR_LEVEL],
                        record[radarAction.RADAR_STATUS],
                        utils.from_unix_timestamp_HHMM(
                            record[radarAction.RADAR_CREATE_AT] / 1000
                        ),
                        record[radarAction.RADAR_COMMANDER],
                    ),
                    record[radarAction.RADAR_ID],
                    valid=True,
                )
        else:
            wf().add_item("no result")
    wf().send_feedback()


if __name__ == "__main__":
    # print(query_all_records())
    sys.exit(wf().run(main))
