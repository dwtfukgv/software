#!/usr/bin/python
# encoding: utf-8
import sys
import shepherdAction 
import utils

from utils import wf, get_args_with_env, Environment


def main(workflow):
    query, mis, cache_seconds, env = get_args_with_env()
    environment = Environment.get_env(env)
    group_list = wf().cached_data(
        "my_shepherd_group_" + env,
        lambda: shepherdAction.groups_list(environment),
        max_age=int(cache_seconds),
    )
    group_list = wf().filter(query, group_list, shepherdAction.key_for_group_record)
    if group_list:
        for group in group_list:
            wf().add_item(
                "{}".format(group[shepherdAction.Group.NAME]),
                "{} - {}".format(
                    group[shepherdAction.Group.PREFIX],
                    group[shepherdAction.Group.DESC],
                ),
                arg="api_group_name={}&api_group_id={}".format(
                    utils.url_encode(group[shepherdAction.Group.NAME]),
                    group[shepherdAction.Group.ID],
                ),
                valid=True,
            )
    else:
        wf().add_item("no result", valid=False)
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
    # delete_cookies(LOG_CENTER_COOKIE_NAME)
