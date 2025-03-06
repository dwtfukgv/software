#!/usr/bin/python
# encoding: utf-8

import getpass
import sys
import init_path
# Workflow3 supports Alfred 3's new features. The `Workflow` class
# is also compatible with Alfred 2.

from utils import wf, get_args
import appkeyAction


def main(workflow):
    query, mis, cache_seconds = get_args()
    # key : deploy name , value : plus id
    plus_dict = workflow.cached_data(
        "plus_releases",
        lambda: appkeyAction.query_plus_by_mis(mis),
        max_age=int(cache_seconds),
    )

    if query:
        plus_list = workflow.filter(query, plus_dict.keys())
    else:
        plus_list = plus_dict.keys()

    if plus_list:
        for release_name in plus_list:
            workflow.add_item(
                release_name,
                arg=plus_dict[release_name],
                largetext=release_name,
                valid=True,
            )
    else:
        workflow.add_item("no result", valid=False)
    workflow.send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
