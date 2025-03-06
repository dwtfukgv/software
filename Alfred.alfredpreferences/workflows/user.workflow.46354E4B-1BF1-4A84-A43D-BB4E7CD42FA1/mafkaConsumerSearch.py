#!/usr/bin/env python
# encoding: utf-8
import sys

import mafkaAction

from utils import wf, get_args


def key_for_record(record):
    return "{} {} {} {}".format(
        record[mafkaAction.NAME],
        record[mafkaAction.APP_KEY],
        record[mafkaAction.TOPIC_NAME],
        record[mafkaAction.REMARK],
    )


def main(workflow):
    query, mis, cache_seconds = get_args()
    if not query:
        query = ""
    mafka_topic_list = mafkaAction.query_paged_consume_group(1, 50, query)
    if mafka_topic_list:
        try:
            mafka_topic_list = mafka_topic_list["data"]["list"]
        except:
            mafka_topic_list = []

    mafka_topic_list = wf().filter(query, mafka_topic_list, key_for_record)
    if mafka_topic_list:
        for record in mafka_topic_list:
            wf().add_item(
                record[mafkaAction.NAME],
                "[{}][{}]{}".format(
                    record[mafkaAction.APP_KEY],
                    record[mafkaAction.TOPIC_NAME],
                    record[mafkaAction.REMARK],
                ),
                record[mafkaAction.ID],
                valid=True,
            )
    else:
        wf().add_item("no result", "", query, valid=True)
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
