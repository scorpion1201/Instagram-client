from . import config
from . import utils
import math
import re
import json
import requests
from urllib.parse import quote_plus as urlencode

__headers = utils.get_headers()
__headers.update({"X-Requested-With": "XMLHttpRequest"})

def get(shortcode=None, headers=None):
    __headers.update({"Referer": "https://www.instagram.com/p/%s/" % (shortcode)})

    headers = __headers if headers is None else headers
    res = requests.get( "https://www.instagram.com/p/%s/?__a=1" % (shortcode), \
                        cookies=config.ig_cookies, \
                        headers=headers )

    if res.status_code is 200 and res.headers["Content-Type"] == "application/json":
        data = res.json()
        media = data["graphql"]["shortcode_media"]

        if media["__typename"] == "GraphSidecar":
            sidecar = list(map(lambda x: x["node"], media["edge_sidecar_to_children"]["edges"]))
            for idx, child in enumerate(sidecar):
                if child["is_video"] is True:
                    child.update({"display_src": child["video_url"]})
                else:
                    child.update({"display_src": child["display_url"]})
                del child["__typename"]
                del child["media_preview"]
                del child["tracking_token"]

            media.update({"sidecar": sidecar})
            del media["edge_sidecar_to_children"]
        elif media["is_video"] is True:
            media.update({"display_src": media["video_url"]})
        else:
            media.update({"display_src": media["display_url"]})

        like_cnt = media["edge_media_preview_like"]["count"]
        comment_cnt = media["edge_media_to_comment"]["count"]
        media.update({"likes": like_cnt, "comments": comment_cnt})

        del media["__typename"]
        del media["media_preview"]
        del media["tracking_token"]

        return media

