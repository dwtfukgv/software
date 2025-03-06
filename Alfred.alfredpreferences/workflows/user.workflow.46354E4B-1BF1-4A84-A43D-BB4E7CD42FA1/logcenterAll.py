#!/usr/bin/python
# encoding: utf-8
import sys
import logcenterAction

from utils import wf, get_args_with_env, Environment


def main(workflow):
    query, mis, cache_seconds, env = get_args_with_env()
    logs = wf().cached_data(
        "all_logs_" + env,
        lambda: logcenterAction.query_all_logs(Environment.get_env(env)),
        max_age=int(cache_seconds),
    )
    logs = wf().filter(query, logs, logcenterAction.key_for_log)
    if logs:
        for log in logs:
            wf().add_item(
                log[logcenterAction.LOG_NAME],
                log[logcenterAction.DESC],
                log[logcenterAction.LOG_NAME],
                valid=True,
            )
    else:
        wf().add_item("no result", valid=False)
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
    # delete_cookies(LOG_CENTER_COOKIE_NAME)
