from .. import config
import requests
import json
from urllib.parse import quote_plus as urlencode

__headers__ = {
    "X-Instagram-AJAX": 1,
    "User-Agent": config.userAgent,
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Referer": "https://www.instagram.com/",
    "Origin":"https://www.instagram.com"
}

query_id = "17874545323001329"
dataType = "count, page_info { end_cursor, has_next_page }, nodes { id, is_verified, followed_by_viewer, requested_by_viewer, full_name, profile_pic_url, username }"

def first( user_id, length ):
    if length >= 50:
        offset = length / pow( 10, ( len( str( length ) ) - 1 ) )
    else:
        offset = 0

    variables = json.dumps(dict(id=str(user_id), first=str((length + offset + 1))))

    payload = "query_id=%s&variables=%s" % (query_id, urlencode(variables),)

    headers = __headers__.copy()
    headers.update({
        "x-csrftoken": config.ig_cookies["csrftoken"],
    })

    res = requests.get( "https://www.instagram.com/graphql/query/?"+payload, \
                         cookies=config.ig_cookies, \
                         headers=headers )

    if res.status_code is 200 and res.headers["Content-Type"] == "application/json":
        return res.json()

def after( user_id, end_cursor, length ):
    query_data = "ig_user(%d) { follows.after(%d) { %s } }" % ( user_id, length, dataType )
    ref_data = "relationships::follow_list"

    payload = { "q": query_data, "ref": ref_data }

    headers = __headers__.copy()
    headers.update({
        "x-csrftoken": config.ig_cookies["csrftoken"],
    })

    res = requests.post( "https://www.instagram.com/query/", \
                         data=payload, \
                         cookies=config.ig_cookies, \
                         headers=headers )

    if res.status_code is 200 and res.headers["Content-Type"] == "application/json":
        return res.json()

def __remake_dist__( data ):
    if type( data ) is not dict: return json.dumps({ "error": 1, "description": "wrong parameter!" }, sort_keys=True, indent=4);


