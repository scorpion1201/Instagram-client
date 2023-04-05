from . import config, utils
import requests

def init():
    __headers = utils.get_headers()

    res = requests.get( "https://www.instagram.com/", headers=__headers )
    config.ig_cookies = dict( csrftoken=res.cookies["csrftoken"], mid=res.cookies["mid"] )

def login(user_id=None, user_pw=None):
    if user_id is None or user_pw is None:
        raise "Instagram account must be necessary."

    config.ig_user_id = user_id
    config.ig_user_pw = user_pw
    headers = {
        "x-csrftoken": config.ig_cookies["csrftoken"],
        "X-Instagram-AJAX": 1,
        "User-Agent": config.userAgent,
        "Referer": "https://www.instagram.com/",
        "Origin": "https://www.instagram.com"
    }
    res = requests.post( "https://www.instagram.com/accounts/login/ajax/", \
                         data={ "username": config.ig_user_id, "password": config.ig_user_pw }, \
                         cookies=config.ig_cookies, \
                         headers=headers )

    if res.headers["Content-Type"] == "application/json":
        data = res.json()
        if not "authenticated" in data:
            print( "no login" )
        elif data["authenticated"]:
            config.ig_sessionId = res.cookies["sessionid"]
            config.ig_uid = res.cookies["ds_user_id"]

            # set cookies
            config.ig_cookies["csrftoken"] = res.cookies["csrftoken"]
            config.ig_cookies["sessionid"] = config.ig_sessionId
            config.ig_cookies["ds_user_id"] = config.ig_uid
            config.ig_cookies["s_network"] = ""

def logout():
    headers = {
        "Origin": "https://www.instagram.com",
        "Referer": "https://www.instagram.com/"
    }

    res = requests.post( "https://www.instagram.com/accounts/logout/", \
                         data={ "csrfmiddlewaretoken": config.ig_cookies["csrftoken"] }, \
                         cookies=config.ig_cookies, \
                         headers=headers )

    if res.status_code == 200:
        config.ig_sessionId = ""
        config.ig_uid = ""

