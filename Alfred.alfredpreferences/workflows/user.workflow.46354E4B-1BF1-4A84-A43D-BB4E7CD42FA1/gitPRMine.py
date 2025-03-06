#!/usr/bin/env python
# encoding: utf-8
import sys

from utils import wf, get_args
import devToolsAction


def key_for_record(record):
    return "{} {} {}".format(
        record[devToolsAction.GIT_APP_KEY],
        record[devToolsAction.SERVICE_ALIAS],
        record[devToolsAction.REPO],
    )


def main(workflow):
    query, mis, cache_seconds = get_args()
    pr_list = devToolsAction.query_my_pr_list()
    pr_list = wf().filter(query, pr_list, key_for_record)
    if pr_list:
        for record in pr_list:
            author = record["author"]
            title = record["title"]
            id = record["id"]
            name = record["name"]
            project_key = record["key"]
            reviewers = record["reviewers"]
            from_branch = record["from_branch"]
            to_branch = record["to_branch"]
            url = "https://dev.sankuai.com/code/repo-detail/{}/{}/pr/{}/diff".format(
                project_key, name, id
            )
            wf().add_item(
                "{} - by {}".format(title, author),
                "[{}][{}]->[{}]".format(reviewers, from_branch, to_branch),
                url,
                valid=True,
            )
    else:
        wf().add_item("no result", "", query, valid=True)
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
