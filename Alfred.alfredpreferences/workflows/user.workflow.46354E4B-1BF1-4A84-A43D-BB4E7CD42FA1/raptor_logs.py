import sys
import raptorAction
from utils import get_args, wf


def key_for_record(record: raptorAction.Log):
    return f"{record.logName} {record.desc} {record.appkey}"


def main(workflow):
    query, mis, cache_seconds = get_args()
    records = wf().cached_data(
        f"raptor_logcenter_my_logs",
        raptorAction.get_all_my_logs,
        max_age=int(cache_seconds),
    )
    records = wf().filter(query, records, key_for_record)
    if records:
        for record in records:
            subtitle = ""
            if record.appkey:
                subtitle = f"[{record.appkey}]:{record.desc}"
            else:
                subtitle = record.desc
            wf().add_item(
                record.logName,
                subtitle,
                arg=record.logName,
                valid=True,
            )
    else:
        wf().add_item("no result")
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
