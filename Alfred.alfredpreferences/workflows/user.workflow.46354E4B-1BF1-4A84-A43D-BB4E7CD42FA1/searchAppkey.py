#!/usr/bin/python
# encoding: utf-8

import sys

import appkeyAction
# Workflow3 supports Alfred 3's new features. The `Workflow` class
# is also compatible with Alfred 2.
from utils import wf


def main(workflow):
    query = None
    if workflow.args:
        query = workflow.args[0]

    app_key_list = appkeyAction.search_appkey(query)

    for app_key in app_key_list:
        workflow.add_item(app_key, arg=app_key, largetext=app_key, valid=True)
    workflow.send_feedback()


if __name__ == '__main__':
    # Call your entry function via `Workflow3.run()` to enable its
    # helper functions, like exception catching, ARGV normalization,
    # magic arguments etc.
    sys.exit(wf().run(main))
