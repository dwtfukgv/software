# -*- coding: utf-8 -*-
# @Time     : 2024/3/29 19:15
# @Author   : liuyulong06
# @File     : mavenSearch.py

"""search maven"""

import sys

from datetime import datetime

import mavenAction

from utils import wf


def main(workflow):
    keyword = wf().args[0]
    component_list = mavenAction.search_maven(keyword)
    for component in component_list:
        wf().add_item(
            component["groupId"] + ":" + component["artifactId"],
            "最近更新："
            + datetime.fromtimestamp(component["timestamp"] / 1000).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            arg=component["groupId"] + ":" + component["artifactId"],
            valid=True,
        )
    if not component_list:
        wf().add_item("no result for " + keyword, valid=False)
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
