import os
import sys

import kmAction
from urllib.request import urlretrieve
import glob
from utils import get_args, wf

mis_avatar_cache_path = "/tmp/alfred_avatar_cache"


def main(workflow):
    query, mis, cache_seconds = get_args()
    records = kmAction.query_users(query)
    cache_path_is_exist = os.path.exists(mis_avatar_cache_path)
    if not cache_path_is_exist:
        os.makedirs(mis_avatar_cache_path)
    to_be_delete_file = set()
    if records:
        for record in records:
            avatar = record["avatar"]
            mis = record["account"]
            icon_path = "{}/{}.jpg".format(mis_avatar_cache_path, mis)
            to_be_delete_file.add(icon_path)
            if avatar:
                urlretrieve(avatar, icon_path)
            wf().add_item(
                "{}-{}".format(mis, record["name"]),
                "{}".format(record["orgNamePath"]),
                mis,
                icon=icon_path,
                valid=True,
            )
    else:
        wf().add_item("no result", valid=False)
    wf().send_feedback()

    for f in glob.glob("{}/*.jpg".format(mis_avatar_cache_path)):
        if f not in to_be_delete_file:
            os.remove(f)


if __name__ == "__main__":
    # print(query_all_records())
    sys.exit(wf().run(main))
