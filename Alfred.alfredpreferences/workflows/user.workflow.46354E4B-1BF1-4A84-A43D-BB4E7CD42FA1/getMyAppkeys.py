#!/usr/bin/python
# encoding: utf-8

import sys
import getpass

# Workflow3 supports Alfred 3's new features. The `Workflow` class
# is also compatible with Alfred 2.
from utils import wf, get_args
import appkeyAction


def main(workflow):
    query, mis, cache_seconds = get_args()
    app_key_list = workflow.cached_data(
        "appkeys",
        lambda: appkeyAction.get_app_key_list(mis),
        max_age=int(cache_seconds),
    )

    if query:
        app_key_list = workflow.filter(
            query,
            app_key_list,
            min_score=1,
        )
        if not app_key_list:
            app_key_list.append(query)

    for app_key in app_key_list:
        workflow.add_item(app_key, arg=app_key, largetext=app_key, valid=True)
    workflow.send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
