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
            service_type = record[devToolsAction.SERVICE_TYPE]
            repo = record[devToolsAction.REPO]
            appkey = record[devToolsAction.GIT_APP_KEY]
            if "MAVEN" == service_type:
                url = "https://dev.sankuai.com/services/{}/to-maven".format(appkey)
            else:
                url = "https://dev.sankuai.com/services/{}/to-deploy/job-list".format(
                    appkey
                )
            wf().add_item(appkey, "[{}]{}".format(service_type, repo), url, valid=True)
    else:
        wf().add_item("no result", "", query, valid=True)
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
