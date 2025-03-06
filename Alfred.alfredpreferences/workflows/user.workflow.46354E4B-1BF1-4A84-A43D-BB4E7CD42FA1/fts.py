import sys

from utils import get_args, from_unix_timestamp, wf


def main(workflow):
    query, mis, cache_seconds = get_args()
    unix_timestamp = int(query.strip().replace(",", ""))
    date_str = from_unix_timestamp(unix_timestamp)
    wf().add_item(date_str, unix_timestamp, date_str, valid=True)
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
