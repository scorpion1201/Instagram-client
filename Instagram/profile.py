from . import config, media
from . import utils
import re
import json
import requests
from urllib.parse import quote_plus as urlencode

__query_id = "17888483320059182"
__headers = utils.get_headers()
__headers.update({"X-Requested-With": "XMLHttpRequest"})

def GetIGViewIndex( username ):
    p = -1
    if config.ig_view != None:
        if len( config.ig_view ) > 0:
            for raw in config.ig_view:
                if username in raw:
                    return p
                p += 1
    return p

def getUserNameById( userId ):
    if config.ig_view != None:
        if len( config.ig_view ) >0:
            for row in config.ig_view:
                for username in row:
                    if row[username]["uid"] == userId:
                        return username

    return ""

def info(username):
    __headers.update({"Referer": "https://www.instagram.com/%s/" % username})

    res = requests.get( "https://www.instagram.com/%s/?__a=1" % username, \
                        cookies=config.ig_cookies, \
                        headers=__headers)
    if res.status_code is 200 and res.headers["Content-Type"] == "application/json":
        user = res.json()["user"]

        raw_idx = GetIGViewIndex( user["username"] )
        if "profile_pic_url_hd" in user: profile_pic = user["profile_pic_url_hd"]
        else: profile_pic = user["profile_pic_url"]

        if raw_idx == -1:
            raw_idx = len( config.ig_view )
            config.ig_view.append({ user["username"]: \
                dict( uid=int(user["id"]), \
                      followed_by=user["followed_by"]["count"], \
                      follows=user["follows"]["count"], \
                      full_name=user["full_name"], \
                      is_private=user["is_private"], \
                      is_verified=user["is_verified"], \
                      profile_url=profile_pic, \
                      username=user["username"], media_count=user["media"]["count"] \
                )})
        else:
            config.ig_view[raw_idx][user["username"]] = \
                dict( uid=int(user["id"]), \
                      followed_by=user["followed_by"]["count"], \
                      follows=user["follows"]["count"], \
                      full_name=user["full_name"], \
                      is_private=user["is_private"], \
                      is_verified=user["is_verified"], \
                      profile_url=profile_pic, \
                      username=user["username"], media_count=user["media"]["count"] \
                )

        return config.ig_view[ raw_idx ][user["username"]]
    elif res.status_code is 404:
        raise "`%s` is empty." % (username)

def media_data(username=None):
    if username is None:
        raise "`username` must be not empty."
    __headers.update({"Referer": "https://www.instagram.com/%s/" % username})

    res = requests.get( "https://www.instagram.com/%s/?__a=1" % username, \
                        cookies=config.ig_cookies, \
                        headers=__headers)
    if res.status_code is 200 and res.headers["Content-Type"] == "application/json":
        user = res.json()["user"]
        if user["is_private"] is True:
            raise "This account is privated."
        return res.json()["user"]["media"]
    elif res.status_code is 404:
        raise "`%s` is empty." % (username)

def first(username=None):
    data = media_data(username)
    new_data = dict(nodes=[],page_info=dict(),)

    __headers.update({"Referer": "https://www.instagram.com/%s/" % username})

    new_data["page_info"] = data["page_info"]
    for idx, row in enumerate(data["nodes"]):
        new_data["nodes"].append(media.get(row["code"], __headers))

    return new_data

def after(user_id, token=None):
    __headers.update({"Referer": "https://www.instagram.com/%s/" % username})
    variables = json.dumps(dict(id=str(user_id), first=12, after=token,))

    payload = "query_id=%s&variables=%s" % (__query_id, urlencode(variables),)

    res = requests.get( "https://www.instagram.com/graphql/query/?"+payload, \
                        cookies=config.ig_cookies, \
                        headers=__headers )

    new_data = dict(nodes=[])

    if res.status_code is 200 and res.headers["Content-Type"] == "application/json":
        data = res.json()

        edge_media = data["data"]["user"]["edge_owner_to_timeline_media"]
        edges = list(map(lambda x: x["node"], edge_media["edges"]))
        new_data.update({"page_info": edge_media["page_info"]})

        for idx, row in enumerate(edges):
            new_data["nodes"].append(media.get(row["shortcode"], __headers))

    return new_data
