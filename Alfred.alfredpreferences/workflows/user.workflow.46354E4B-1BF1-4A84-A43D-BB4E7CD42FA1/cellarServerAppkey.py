#!/usr/bin/env python
# encoding: utf-8
import json
import sys

from utils import wf, get_args
import cellarAction


def main(workflow):
    query, mis, cache_seconds = get_args()
    if query:
        # Use the new search_server_appkey method when a query is provided
        cluster_detail = cellarAction.get_cluster_details(query)
        if cluster_detail:
            print(cluster_detail["id"], end="")


if __name__ == "__main__":
    sys.exit(wf().run(main))
