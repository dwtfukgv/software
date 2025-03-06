#!/usr/bin/env python
# encoding: utf-8
import sys

import squirrelAction

from utils import wf, get_args


def main(workflow):
    query, mis, cache_seconds = get_args()
    squirrel_cluster_list = squirrelAction.query_resource(query, "Group")
    if squirrel_cluster_list:
        for cluster in squirrel_cluster_list:
            wf().add_item(
                cluster["resourceName"],
                "[{}]-{}".format(cluster["ownerName"], cluster["description"]),
                cluster["resourceName"],
                valid=True,
            ),

    else:
        wf().add_item("no result")
    workflow.send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
