from . import config

def get_headers(method="GET"):
    headers = {
        "Accept": "*/*",
        "Accept-Language": "ko,en-US;q=0.9,en;q=0.8",
        "User-Agent": config.userAgent
    }

    if config.ig_cookies is not None:
        headers.update({"x-csrftoken": config.ig_cookies["csrftoken"]})

    if method.lower() is "post":
        headers.update({
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        })
    
    return headers
