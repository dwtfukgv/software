#!/usr/bin/python
# encoding: utf-8
import sys

import domainAction
from utils import get_args, wf


def key_for_record(record):
    return "{} {} {} {} {}".format(
        record[domainAction.DOMAIN_FULLNAME],
        record[domainAction.DOMAIN_NET],
        record[domainAction.DOMAIN_ENV],
        record[domainAction.DOMAIN_KIND],
        record[domainAction.DOMAIN_DESC],
    )


def main(workflow):
    query, mis, cache_seconds = get_args()
    records = workflow.cached_data(
        "domain_my_list_cache", domainAction.query_my_domain, max_age=int(cache_seconds)
    )
    records = wf().filter(query, records, key_for_record)
    if records:
        for record in records:
            wf().add_item(
                record[domainAction.DOMAIN_FULLNAME],
                "[{}][{}]-{}".format(
                    record[domainAction.DOMAIN_ENV],
                    record[domainAction.DOMAIN_NET],
                    record[domainAction.DOMAIN_DESC],
                ),
                record[domainAction.DOMAIN_FULLNAME],
                valid=True,
            )
    else:
        wf().add_item("no result")
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
