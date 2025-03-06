# -*- coding: utf-8 -*-
# @Time     : 2024/3/24 16:34
# @Author   : liuyulong06
# @File     : shepherdSearch.py

"""search shepherd api and api group"""

import sys

import shepherdAction

from utils import wf, get_args_with_env, Environment


def main(workflow):
    keyword, mis, cache_seconds, env = get_args_with_env()
    environment = Environment.get_env(env)
    api_groups, apis = shepherdAction.search_shepherd(keyword, environment)
    for api_group in api_groups:
        wf().add_item(
            "ApiGroup: " + api_group["apiGroupName"],
            "ApiGroup",
            arg=shepherdAction.build_api_group_url(api_group),
            valid=True,
        )
    for api in apis:
        wf().add_item(
            "Api: " + api["apiName"],
            "ApiGroup: " + api["apiGroupName"],
            arg=shepherdAction.build_api_detail_url(api),
            valid=True,
        )
    if not api_groups and not apis:
        wf().add_item("no result for " + keyword)

    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
