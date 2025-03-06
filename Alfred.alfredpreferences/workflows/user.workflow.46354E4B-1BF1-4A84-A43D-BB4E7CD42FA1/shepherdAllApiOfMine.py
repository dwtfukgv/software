#!/usr/bin/python
# encoding: utf-8
import sys
from utils import wf, get_args_with_env, url_encode, Environment
import shepherdAction
from typing import List, Dict


def main(workflow):
    query, mis, cache_seconds, env = get_args_with_env()

    # Convert string env to Environment enum
    environment = Environment.get_env(env)

    all_my_api_list = wf().cached_data(
        f"my_all_shepherd_apis_{env}",
        lambda: shepherdAction.all_my_api_list(environment),
        max_age=int(cache_seconds),
    )

    all_my_api_list = wf().filter(query, all_my_api_list, shepherdAction.key_for_api_record)

    if all_my_api_list:
        for api in all_my_api_list:
            api_query = (
                f"api_group_name={url_encode(api[shepherdAction.API.GROUP_NAME])}"
                f"&api_group_id={api[shepherdAction.API.GROUP_ID]}"
                f"&group_tab=api-manage"
                f"&api_name={url_encode(api[shepherdAction.API.NAME])}"
                f"&api_id={api[shepherdAction.API.ID]}"
            )
            wf().add_item(
                f"{api[shepherdAction.API.PATH]}",
                f"{api[shepherdAction.API.NAME]} - {api[shepherdAction.API.DESC]}",
                arg=api_query,
                valid=True,
            )
    else:
        wf().add_item("No result", valid=False)

    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
