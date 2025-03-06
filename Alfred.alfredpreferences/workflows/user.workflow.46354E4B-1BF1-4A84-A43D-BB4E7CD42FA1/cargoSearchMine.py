#!/usr/bin/env python
# encoding: utf-8
import sys

import devToolsAction

from utils import wf, get_args


def key_for_record(record):
    return "{} {}".format(record[devToolsAction.NAME], record[devToolsAction.SWIMLANE])


def main(workflow):
    query, mis, cache_seconds = get_args()
    cargo_list = workflow.cached_data(
        "cargo_my_list_cache",
        lambda: devToolsAction.query_my_all_cargos(10),
        max_age=int(cache_seconds),
    )

    cargo_list = wf().filter(query, cargo_list, key_for_record)
    if cargo_list:
        for record in cargo_list:
            wf().add_item(
                record[devToolsAction.NAME],
                "[{}][服务数:{}]-{}".format(
                    record[devToolsAction.MACHINE_ENV],
                    record[devToolsAction.SERVICE_COUNT],
                    (
                        record[devToolsAction.SWIMLANE]
                        if record[devToolsAction.SWIMLANE]
                        else "主干"
                    ),
                ),
                record[devToolsAction.STACK_UUID],
                valid=True,
            )
    else:
        wf().add_item("no result", "", query, valid=True)
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
