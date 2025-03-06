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
        results = cellarAction.search_server_appkey(query)
        if results:
            for appkey in results:
                workflow.add_item(title=appkey, arg=appkey, valid=True)
        else:
            workflow.add_item(title="No results found", valid=False)
    workflow.send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
