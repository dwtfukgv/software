#!/usr/bin/python
# encoding: utf-8
import sys

import rdsAction
from utils import get_args_with_env, wf, Environment


def key_for_record(record):
    return "{} {}".format(record[rdsAction.DATABASE_NAME], record[rdsAction.DESC])


def main(workflow):
    import os

    cluster_id = os.getenv("cluster_id")
    query, mis, cache_seconds, env = get_args_with_env()
    wf().logger.info(f"cluster_id:{cluster_id}")
    records = wf().cached_data(
        "my_rds_database_{}_{}".format(env, cluster_id),
        lambda: rdsAction.query_databases_by_cluster_id(cluster_id, Environment.get_env(env)),
        max_age=int(cache_seconds),
    )
    records = wf().filter(query, records, key_for_record)
    if records:
        for record in records:
            wf().add_item(
                record[rdsAction.DATABASE_NAME],
                record[rdsAction.DESC],
                record[rdsAction.DATABASE_ID],
                valid=True,
            )
    else:
        wf().add_item("no result")
    wf().send_feedback()


if __name__ == "__main__":
    # print(query_all_records())
    sys.exit(wf().run(main))
