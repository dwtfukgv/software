#!/usr/bin/env python
# encoding: utf-8
import sys

import devToolsAction

from utils import wf, get_args


def key_for_record(record):
    return "{} {}".format(record[devToolsAction.NAME], record[devToolsAction.SWIMLANE])


def main(workflow):
    query, mis, cache_seconds = get_args()
    cargo_list = devToolsAction.search_cargos(query)
    cargo_list_by_name = devToolsAction.search_cargos(query, type="stack_name")
    if cargo_list_by_name:
        cargo_list.extend(cargo_list_by_name)

    cargo_list = wf().filter(query, cargo_list, key_for_record)
    if cargo_list:
        for record in cargo_list:
            if record[devToolsAction.SWIMLANE]:
                swimlane = record[devToolsAction.SWIMLANE]
            else:
                swimlane = "主干"

            wf().add_item(
                "{}|{}".format(record[devToolsAction.NAME], swimlane),
                "[{}|服务数:{}]{}".format(
                    record[devToolsAction.MACHINE_ENV],
                    record[devToolsAction.SERVICE_COUNT],
                    swimlane,
                ),
                record[devToolsAction.STACK_UUID],
                valid=True,
            )
    else:
        wf().add_item("no result", "", query, valid=True)
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
