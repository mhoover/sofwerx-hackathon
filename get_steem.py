#!/usr/bin/python
import base64
import httplib
import json
import requests
import urllib

from bs4 import BeautifulSoup

steem_trending = requests.get('https://steemit.com/trending')
steem_soup = BeautifulSoup(steem_trending.content, 'html.parser')
steem_json = json.loads(steem_soup.find('script', type='application/json').text)

# some things to remember
# steem_json['global'] is really the only key with anything
# steem_json['global']['accounts'] is the important object; keys are user names
# steem_json['global']['content'] contains the info wanted



# microsoft azure emotion api
headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': os.getenv('MSFT_EMOTION1'),
}
params = urllib.urlencode({
})
# loop over images below
body = str({'url': '{}'.format('http://static.wixstatic.com/media/f38d6ceaec14d8857cac48673dab8878.jpg')})

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
