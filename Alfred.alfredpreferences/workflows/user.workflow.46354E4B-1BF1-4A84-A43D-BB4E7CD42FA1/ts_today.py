import sys
from datetime import datetime

from utils import get_args, from_unix_timestamp, to_unix_timestamp, wf


def main(workflow):
    today_str = datetime.today().strftime("%Y-%m-%d")
    today = to_unix_timestamp(today_str)
    wf().add_item(today, today_str, today, valid=True)
    wf().send_feedback()


if __name__ == '__main__':
    sys.exit(wf().run(main))
