#!/usr/bin/env python -u

from time import sleep
import urllib
import json
import requests
import requests.auth
import argparse

# To generate application id and secret key, see 
# https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example
parser = argparse.ArgumentParser(description="Download Reddit comments")
parser.add_argument("--user",       help="Reddit username")
parser.add_argument("--password",   help="Reddit password")
parser.add_argument("--app",        help="OAuth2 application id")
parser.add_argument("--secret",     help="OAuth2 secret key")
parser.add_argument("--user-agent", help="OAuth2 secret key", default=None)
args = parser.parse_args()

if args.user_agent is None:
    args.user_agent = "reddit-hist/%s" % args.user

client_auth = requests.auth.HTTPBasicAuth(args.app, args.secret)
post_data = {
    "grant_type" : "password", 
    "username"   : args.user, 
    "password"   : args.password }
headers = {"User-Agent": args.user_agent}
response = requests.post("https://www.reddit.com/api/v1/access_token", 
                         auth=client_auth, 
                         data=post_data, 
                         headers=headers)
print response.json()

access_token = response.json()["access_token"]
token_type = response.json()["token_type"]
auth = "%s %s" % (token_type, access_token)

headers = {"Authorization": auth, "User-Agent": args.user_agent}
response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
print json.dumps(response.json(), indent=4, sort_keys=True)

nextTag = None
count = 0
long_wait_sec = 300

while True:
    url = "https://oauth.reddit.com/user/%s/comments" % args.user
    if nextTag is not None:
        url += "?after=%s&count=%d" % (nextTag, count)
        
    # print "calling:"
    # print "  url:       %s" % url
    # print "  headers:   %s" % headers
    response = requests.get(url, headers=headers)
    content = response.json()

    # dump output
    if content is not None:
        if "data" in content:
            if "after" in content["data"]:
                nextTag = content["data"]["after"]
                children = content["data"]["children"]
                count += len(children)
                print json.dumps(children, indent=2, sort_keys=True)
                print ""
                print "waiting before loading next page (%s)" % nextTag
                sleep(5)
                continue
    
    print "unable to parse response: %s" % content
    print "sleeping %d sec..." % long_wait_sec
    sleep(long_wait_sec)

print "done"
