import sys


import raptorAction
from utils import get_args, wf


def key_for_record(record: raptorAction.FrontProject):
    return record.domain


def main(workflow):
    query, mis, cache_seconds = get_args()
    raptor_front_projects = wf().cached_data(
        "raptor_front_projects",
        raptorAction.get_front_project,
        max_age=int(cache_seconds),
    )
    raptor_front_projects = wf().filter(query, raptor_front_projects, key_for_record)
    if raptor_front_projects:
        for p in raptor_front_projects:
            wf().add_item(
                p.domain, "", json.dumps({"id": p.id, "domain": p.domain}), valid=True
            )
    else:
        wf().add_item("no result", valid=False)
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
