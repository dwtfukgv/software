#!/usr/bin/python
# encoding: utf-8

import getpass
import sys
from utils import wf, get_args
import appkeyAction

def main(workflow):
    query, mis, cache_seconds = get_args()
    app_key_list = workflow.cached_data(
        "appkeys",
        lambda: appkeyAction.get_app_key_list(mis),
        max_age=int(cache_seconds),
    )
    app_key_repository_dict = workflow.cached_data(
        "appkeys_repository",
        lambda: appkeyAction.get_git_repositoy(app_key_list),
        max_age=int(cache_seconds),
    )
    if query:
        app_key_list = workflow.filter(query, app_key_list)
        if not app_key_list:
            app_key_list.append(query)

    for app_key in app_key_list:
        git_path = None
        if app_key in app_key_repository_dict:
            git_path = app_key_repository_dict[app_key]
            workflow.add_item(app_key, arg=git_path, largetext=app_key, valid=True)
    workflow.send_feedback()


if __name__ == "__main__":
    # Call your entry function via `Workflow3.run()` to enable its
    # helper functions, like exception catching, ARGV normalization,
    # magic arguments etc.
    sys.exit(wf().run(main))
