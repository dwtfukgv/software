import sys

import diggerAction
from utils import get_args, wf


def key_for_record(record):
    return record["name"]


def main(workflow):
    query, mis, cache_seconds = get_args()
    records = diggerAction.query_dashboard(query)
    if records:
        for d in records:
            wf().add_item(d["name"], "", d["id"], valid=True)
    else:
        wf().add_item("no result", valid=False)
    wf().send_feedback()


if __name__ == "__main__":
    # print(query_all_records())
    sys.exit(wf().run(main))
