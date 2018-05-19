from requests_oauthlib import OAuth1Session
import config
import json

def init():
    CK = config.CK
    CS = config.CS
    AT = config.AT
    AS = config.AS

    return OAuth1Session(CK, CS, AT, AS)

def get_mentions(oauth, since_id):
    url = "https://api.twitter.com/1.1/statuses/mentions_timeline.json"

    params = {
        "since_id" : since_id
    }

    request = oauth.get(url, params=params)

    if request.status_code == 200:
        return json.loads(request.text)
    else:
        print("Error> get_mentions : " + str(request.status_code))
        return None

def result_reply(oauth, results):
    url = "https://api.twitter.com/1.1/statuses/update.json"

    for result in results:

        params = {
            "status" : "@" + result["screen_name"] + " " + result["result"],
            "in_reply_to_status_id" : result["id"]
        }

        request = oauth.post(url, params=params)

        if request.status_code == 200:
            print("result_reply : OK")
        else:
            print("Error> result_reply : " + str(request.status_code))
