import sys

import kmAction
from utils import get_args, wf


def main(workflow):
    query, mis, cache_seconds = get_args()
    wf().logger.info(query)
    dx_uid = kmAction.query_dxuid(query)
    print(dx_uid, end='')


if __name__ == '__main__':
    # print(query_all_records())
    sys.exit(wf().run(main))
