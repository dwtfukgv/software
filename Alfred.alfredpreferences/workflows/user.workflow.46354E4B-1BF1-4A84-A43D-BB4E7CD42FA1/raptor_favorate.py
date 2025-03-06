#!/usr/bin/python
import sys
import raptorAction
from utils import get_args, wf


def key_for_record(record: raptorAction.Dashboard):
    return record.name


def main(workflow):
    query, mis, cache_seconds = get_args()
    favorite_dashboards = wf().cached_data(
        "raptor_dashboard_favorite",
        raptorAction.my_favorate_dashboard,
        max_age=int(cache_seconds),
    )
    favorite_dashboards = wf().filter(query, favorite_dashboards, key_for_record)
    if favorite_dashboards:
        for d in favorite_dashboards:
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
