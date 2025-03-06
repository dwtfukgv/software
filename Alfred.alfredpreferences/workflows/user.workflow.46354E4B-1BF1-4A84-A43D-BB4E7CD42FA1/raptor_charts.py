import sys

import sys

import raptorAction
from utils import get_args, wf


def key_for_record(record: raptorAction.Chart):
    return record.name


def main(workflow):
    import os

    # rpt_dashboard_id_iscore : dashboard=234&isCore=false
    dashboard_info = os.getenv("rpt_dashboard_id_iscore")
    dashboard_id_query, is_core_query = dashboard_info.split("&")
    dashboard_id = dashboard_id_query.split("=")[1]
    is_core = is_core_query.split("=")[1]
    wf().logger.info("dashboard_id:%s", dashboard_id)
    query, mis, cache_seconds = get_args()
    records = wf().cached_data(
        f"raptor_dashboard_{is_core}_{dashboard_id}",
        lambda: raptorAction.get_charts_by_dashboard(dashboard_id, is_core == "true"),
        max_age=int(cache_seconds),
    )
    records = wf().filter(query, records, key_for_record)
    if records:
        for record in records:
            wf().add_item(
                record.name,
                arg=record.id,
                valid=True,
            )
    else:
        wf().add_item("no result")
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
