#!/usr/bin/env python
import sys
import init_path
from utils import get_args, wf
import avatarAction

AVATAR_HOST_URL = "https://avatar.mws.sankuai.com/#/service/detail/host?"
AVATAR_VIP_URL = "https://avatar.mws.sankuai.com/#/service/detail/oceanus?"


def main(workflow):
    query, mis, cache_seconds = get_args()
    if query:
        records = avatarAction.query_services(query.strip())
        wf().logger.info(f"records: {records}")
        for s in records:
            path = f"appkey={s.appkey}&env={s.env}"
            if s.resourceType == "VIP":
                url = AVATAR_VIP_URL + path + "&tab=mgw"
            else:
                url = AVATAR_HOST_URL + path
            wf().add_item(s.appkey, f"【{s.env}】{s.appkey}", arg=url, valid=True)
        wf().send_feedback()


if __name__ == "__main__":
    # print(query_all_records())
    sys.exit(wf().run(main))
