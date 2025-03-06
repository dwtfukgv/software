# -*- coding: utf-8 -*-
# @Time     : 2024/3/29 19:29
# @Author   : liuyulong06
# @File     : mavenSearchDetail.py

"""search maven"""

import sys

from datetime import datetime

import mavenAction

from utils import wf


def main(workflow):
    keyword = wf().args[0]
    if not keyword or ":" not in keyword:
        wf().add_item("请输入正确的组件格式，如com.android.support:support-v4")
        return
    component_list = mavenAction.search_maven_detail(*keyword.split(":"))

    if not component_list:
        wf().add_item("no result for " + keyword, valid=False)
        wf().send_feedback()
        return

    component = component_list[0]
    for version in component["versions"]:
        wf().add_item(
            version["version"],
            "最后更新：{}, 发布人：{}".format(
                datetime.fromtimestamp(version["timestamp"] / 1000).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                version["author"],
            ),
            arg="{}/{}/{}".format(
                component["groupId"], component["artifactId"], version["version"]
            ),
            valid=True,
        )
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
