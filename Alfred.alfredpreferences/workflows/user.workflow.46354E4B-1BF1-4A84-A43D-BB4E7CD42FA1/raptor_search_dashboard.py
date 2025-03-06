import json
# encoding: utf-8
import sys

import raptorAction
from utils import get_args, wf


def key_for_record(record: raptorAction.Dashboard):
    return record.name


def main(workflow):
    query, mis, cache_seconds = get_args()
    dashboard_rows = []
    result = raptorAction.search_dashboard(query, True)
    if result:
        dashboard_rows.extend(result)
    result = raptorAction.search_dashboard(query, False)
    if result:
        dashboard_rows.extend(result)

    if dashboard_rows:
        for d in dashboard_rows:
            is_core = str(d.is_core).lower()
            wf().add_item(
                d.name,
                d.org,
                f"dashboard={d.id}&isCore={is_core}",
                valid=True,
            )
    else:
        wf().add_item("no result", valid=False)
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
