from . import config, media
from . import utils
import re
import json
import requests
from datetime import datetime
from urllib.parse import quote_plus as urlencode

__query_id = "17875800862117404"
__headers = utils.get_headers()
__headers.update({"X-Requested-With": "XMLHttpRequest"})

def tag_data(tagname=None):
    if tagname is None:
        raise "`tagname` must be not empty."

    tag_url = "https://www.instagram.com/explore/tags/%s/" % urlencode(tagname)
    __headers.update({"Referer": tag_url})

    res = requests.get( tag_url + "?__a=1", \
                        cookies=config.ig_cookies, \
                        headers=__headers)

    if res.status_code is 200 and res.headers["Content-Type"] == "application/json":
        return res.json()
    elif res.status_code is 404:
        raise "`%s` is empty." % (tagname)

def first(tagname=None):
    data = tag_data(tagname)
    new_data = dict(name=data["tag"]["name"], nodes=[], page_info=dict(),)

    tag_url = "https://www.instagram.com/explore/tags/%s/" % urlencode(tagname)
    __headers.update({"Referer": tag_url})

    new_data["page_info"] = data["tag"]["media"]["page_info"]
    new_data.update({"count": data["tag"]["media"]["count"]})
    top_posts = data["tag"]["top_posts"]["nodes"]

    top_post_ids = list(map(lambda x: x["id"], top_posts))

    for idx, row in enumerate(top_posts):
        row.update({"taken_at_timestamp": row["date"]})
        row.update({"shortcode": row["code"]})
        row["likes"] = row["likes"]["count"]
        row["comments"] = row["comments"]["count"]
        del row["code"]
        del row["date"]
        new_data["nodes"].append(row)

    for idx, row in enumerate(data["tag"]["media"]["nodes"]):
        if (row["id"] in top_post_ids) is not True:
            row.update({"taken_at_timestamp": row["date"]})
            row.update({"shortcode": row["code"]})
            row["likes"] = row["likes"]["count"]
            row["comments"] = row["comments"]["count"]
            del row["code"]
            del row["date"]
            new_data["nodes"].append(row)

    return new_data

def after(tagname=None, token=None):
    if tagname is None:
        raise "`tagname` must be not empty."

    if token is None:
        raise "`token` must be not empty."

    tag_url = "https://www.instagram.com/explore/tags/%s/" % urlencode(tagname)
    __headers.update({"Referer": tag_url})

    variables = json.dumps(dict(tag_name=str(tagname), first=258, after=token,))
    payload = "query_id=%s&variables=%s" % (__query_id, urlencode(variables),)

    res = requests.get( "https://www.instagram.com/graphql/query/?"+payload, \
                        cookies=config.ig_cookies, \
                        headers=__headers )

    new_data = dict(nodes=[],)
    if res.status_code is 200 and res.headers["Content-Type"] == "application/json":
        data = res.json()

        edge_media = data["data"]["hashtag"]["edge_hashtag_to_media"]
        edge_top_posts = data["data"]["hashtag"]["edge_hashtag_to_top_posts"]
        edges = list(map(lambda x: x["node"], edge_media["edges"]))
        top_post_ids = list(map(lambda x: x["node"]["id"], edge_top_posts["edges"]))

        new_data.update({"page_info": edge_media["page_info"]})

        for idx, row in enumerate(edges):
            if (row["id"] in top_post_ids) is not True:
                row.update({"likes": row["edge_liked_by"]["count"]})
                row.update({"comments": row["edge_media_to_comment"]["count"]})
                del row["edge_liked_by"]
                del row["edge_media_to_comment"]
                new_data["nodes"].append(row)

    return new_data

def gets(tagname):
    data = first(tagname)
    if data["page_info"]["has_next_page"] is not True:
        return data

    while data["page_info"]["has_next_page"]:
        token = data["page_info"]["end_cursor"]

        tmp = after(tagname, token)
        data["nodes"] = data["nodes"] + tmp["nodes"]
        data["page_info"] = tmp["page_info"]

    return data

