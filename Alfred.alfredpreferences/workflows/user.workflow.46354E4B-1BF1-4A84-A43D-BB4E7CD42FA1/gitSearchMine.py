#!/usr/bin/env python
# encoding: utf-8
import sys

import devToolsAction

from utils import wf, get_args


def key_for_record(record):
    return "{} {} {}".format(
        record[devToolsAction.GIT_APP_KEY],
        record[devToolsAction.SERVICE_ALIAS],
        record[devToolsAction.REPO],
    )


def main(workflow):
    query, mis, cache_seconds = get_args()
    repo_list = workflow.cached_data(
        "repo_my_list_cache",
        lambda: devToolsAction.query_my_all_code_repos(10),
        max_age=int(cache_seconds),
    )
    repo_list = wf().filter(query, repo_list, key_for_record)
    if repo_list:
        for record in repo_list:
            wf().add_item(
                record[devToolsAction.GIT_APP_KEY],
                "[{}]{}".format(
                    record[devToolsAction.SERVICE_TYPE], record[devToolsAction.REPO]
                ),
                record[devToolsAction.REPO],
                valid=True,
            )
    else:
        wf().add_item("no result", "", query, valid=True)
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
