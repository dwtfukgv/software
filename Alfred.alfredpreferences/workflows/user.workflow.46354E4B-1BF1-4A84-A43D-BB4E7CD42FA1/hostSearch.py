import sys

import raptorAction
from utils import get_args, wf


def main(workflow):
    query, mis, cache_seconds = get_args()
    if query:
        records = raptorAction.query_host(query.strip())
        if records:
            for record in records:
                wf().add_item(
                    record.ip,
                    record.hostname,
                    f"host_ip={record.ip}&host_name={record.hostname}",
                    valid=True,
                )
        else:
            wf().add_item("no result", valid=False)
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
