#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import kmAction
from workflow import Workflow3
from utils import get_args, wf

KM_SEARCH_OLD_ARG = 'km_search_oldArg'
KM_SEARCH_OLD_RESULT = 'km_search_oldResult'


def main(workflow):
    query, mis, cache_seconds = get_args()

    if query:
        old_arg = os.getenv(KM_SEARCH_OLD_ARG)
        old_result = os.getenv(KM_SEARCH_OLD_RESULT)
        if old_arg != query:
            wf().rerun = 0.1
            wf().setvar(KM_SEARCH_OLD_ARG, query)
            wf().setvar(KM_SEARCH_OLD_RESULT, old_result)
            result = [query]
            if old_result:
                result.extend(old_result.split(','))
            add_items(result)
        else:
            new_result = kmAction.suggest(query)
            wf().setvar(KM_SEARCH_OLD_ARG, query)
            wf().setvar(KM_SEARCH_OLD_RESULT, ','.join(new_result))
            result = [query]
            if new_result:
                result.extend([name for name in new_result if name != query])
            add_items(result)
    else:
        records = kmAction.search_history()
        add_items(records)

    wf().send_feedback()


def add_items(suggest_list):
    if suggest_list:
        for name in suggest_list:
            wf().add_item(name, f'搜索学城：{name}', arg=name, valid=True)


if __name__ == '__main__':
    sys.exit(wf().run(main))
