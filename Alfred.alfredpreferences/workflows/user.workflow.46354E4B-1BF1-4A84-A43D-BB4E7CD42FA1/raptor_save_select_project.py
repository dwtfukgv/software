# coding=utf-8
import json
import os
import sys

from utils import get_args, wf


def main(workflow):
    current_front_project = os.getenv("current_front_project")
    project = json.loads(current_front_project)
    # python3中存储序列化按照utf8编码持久化
    wf().store_data(
        "current_selected_front_project", current_front_project.encode("utf-8")
    )
    wf().logger.info(f"current project {current_front_project} {project}")
    wf().add_item(
        f"raptor前端项目设置为{project['domain']}",
        valid=True,
    )
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
