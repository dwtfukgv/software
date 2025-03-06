#!/usr/bin/env python
# encoding: utf-8
import sys

import mafkaAction

from utils import wf, get_args


def key_for_record(record):
    return "{} {} {} {}".format(
        record[mafkaAction.ID],
        record[mafkaAction.NAME],
        record[mafkaAction.APP_KEY],
        record[mafkaAction.REMARK],
    )


def main(workflow):
    query, mis, cache_seconds = get_args()
    mafka_topic_list = workflow.cached_data(
        "mafka_topic_list_cache",
        lambda: mafkaAction.query_all_topics(20),
        max_age=int(cache_seconds),
    )
    mafka_topic_list = wf().filter(query, mafka_topic_list, key_for_record)
    if mafka_topic_list:
        for record in mafka_topic_list:
            wf().add_item(
                record[mafkaAction.NAME],
                "[{}]{}".format(
                    record[mafkaAction.APP_KEY], record[mafkaAction.REMARK]
                ),
                record[mafkaAction.ID],
                valid=True,
            )
    else:
        wf().add_item(query, "", query, valid=True)
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
