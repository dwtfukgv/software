#!/usr/bin/python
# encoding: utf-8
import sys

import coeAction
from utils import get_args, wf


def main(workflow):
    query, mis, cache_seconds = get_args()
    incidents = coeAction.search_coe(query)
    if incidents:
        for i in incidents:
            coe_level = i[coeAction.LEVEL]
            occur_time = i[coeAction.OCCUR_TIME]
            if occur_time:
                occur_time = occur_time.split(" ")[0]
            if not coe_level:
                coe_level = "未定级"
            wf().add_item(
                "[{}]{}".format(coe_level, i[coeAction.BRIEF]),
                "[{}]{}".format(occur_time, i[coeAction.ORG_PATH]),
                i[coeAction.INCIDENT_ID],
                valid=True,
            )
    else:
        wf().add_item("no result", valid=False)
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
