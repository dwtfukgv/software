#!/usr/bin/python
# encoding: utf-8

import json
import sys

from webUtils import post_form, get



def get_app_key_list(mis):
    params = dict(mis=mis)
    return post_form(
        "http://b.gateway.waimai.st.sankuai.com/api/open/appkeysByMis", data=params
    )


def get_git_repositoy(app_key_list):
    params = dict(appkeys=",".join(app_key_list))
    return post_form(
        "http://b.gateway.waimai.st.sankuai.com//api/open/appkeys/git", data=params
    )


def search_appkey(keyword):
    params = dict(keyword=keyword)
    return post_form(
        "http://b.gateway.waimai.st.sankuai.com/api/open/searchAppkeys", data=params
    )


def query_mis_by_appkey(appkey):
    params = dict(appkey=appkey)
    return post_form(
        "http://b.gateway.waimai.st.sankuai.com/api/open/queryMisByAppkey", data=params
    )


def query_plus_by_mis(mis):
    result = {}
    resp = get("http://plus.sankuai.com/release/list/{mis}".format(mis=mis))
    release_names = resp.keys()
    for release_name in release_names:
        resp = get("http://plus.sankuai.com//release_id/{0}".format(release_name))
        result[release_name] = resp["Id"]
    return result


if __name__ == "__main__":
    json_data = get_app_key_list("pingxumeng")
    print(json_data)
