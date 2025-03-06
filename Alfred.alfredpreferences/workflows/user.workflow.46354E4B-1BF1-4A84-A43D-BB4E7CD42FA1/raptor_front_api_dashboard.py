#!/usr/bin/python
# encoding: utf-8
import json
import sys

import raptorAction
from utils import get_args, wf


def key_for_record(record: raptorAction.Api):
    return f"{record.name} {record.title}"


def main(workflow):
    query, mis, cache_seconds = get_args()
    current_selected_front_project = wf().stored_data("current_selected_front_project")
    if not current_selected_front_project:
        raise RuntimeError("请先运行cfp指令，选择前端项目")
    # python3中存储序列化按照utf8编码持久化
    raptor_front_project = json.loads(current_selected_front_project.decode("utf-8"))
    project_id = raptor_front_project["id"]
    project_domain = raptor_front_project["domain"]
    api_list = wf().cached_data(
        f"raptor_front_project_{project_id}",
        lambda: raptorAction.get_api_by_project(project_id),
        max_age=int(cache_seconds),
    )
    api_list = wf().filter(query, api_list, key_for_record)
    if api_list:
        for record in api_list:
            wf().add_item(
                record.name,
                f"[{project_domain}] {record.title}",
                f"projectId={project_id}&apiId={record.id}",
                valid=True,
            )
    else:
        wf().add_item("no result")
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
