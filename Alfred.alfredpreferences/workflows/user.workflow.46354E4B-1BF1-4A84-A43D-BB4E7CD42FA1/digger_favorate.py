import sys

import diggerAction
from utils import get_args, wf


def key_for_record(record):
    return record["name"]


def main(workflow):
    query, mis, cache_seconds = get_args()
    favorite_dashboards = wf().cached_data(
        "digger_favorite", diggerAction.get_favourite, max_age=int(cache_seconds)
    )
    favorite_dashboards = wf().filter(query, favorite_dashboards, key_for_record)
    if favorite_dashboards:
        for d in favorite_dashboards:
            wf().add_item(d["name"], "", d["id"], valid=True)
    else:
        wf().add_item("no result", valid=False)
    wf().send_feedback()


if __name__ == "__main__":
    # print(query_all_records())
    sys.exit(wf().run(main))
