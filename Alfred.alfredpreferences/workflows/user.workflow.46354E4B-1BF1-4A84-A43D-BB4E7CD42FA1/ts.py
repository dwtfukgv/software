import sys

from utils import get_args, to_unix_timestamp, wf


def main(workflow):
    query, mis, cache_seconds = get_args()
    unix_timestamp = to_unix_timestamp(query.strip())
    wf().add_item(unix_timestamp, query, unix_timestamp, valid=True)
    wf().send_feedback()


if __name__ == '__main__':
    sys.exit(wf().run(main))
