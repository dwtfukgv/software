import sys
from datetime import datetime

from utils import get_args, from_unix_timestamp, to_unix_timestamp, wf


def main(workflow):
    now_str = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    now = to_unix_timestamp(now_str)
    wf().add_item(now, now_str, now, valid=True)
    wf().send_feedback()


if __name__ == '__main__':
    sys.exit(wf().run(main))
