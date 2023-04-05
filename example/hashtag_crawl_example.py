#-*- coding: utf-8 -*-
from Instagram import hashtag
import json

def hashtag_crawl(tagname):
    data = hashtag.first(tagname)
    if data["page_info"]["has_next_page"] is not True:
        return data

    #until last JSON data
    while data["page_info"]["has_next_page"]:
        token = data["page_info"]["end_cursor"]

        #fetch next JSON data from Instagram
        tmp = hashtag.after(tagname, token)
        data["nodes"] = data["nodes"] + tmp["nodes"]
        data["page_info"] = tmp["page_info"]

    return data

if __name__ == "__main__":
    data = hashtag_crawl("나불돈")
    print(json.dumps(data, indent=4, sort_keys=True))
