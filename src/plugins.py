import pprint
import requests
import json

import lxml.html
import re

def strip_tag(s):
    doc = lxml.html.fromstring(s)   # parse html string
    txt = doc.xpath('text()')       # ['foo ', ' bar']
    txt = ' '.join(txt)             # 'foo   bar'
    return re.sub('\s+', ' ', txt)  # 'foo bar'


def google(searchfor=''):
    link = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&{}'.format(searchfor)
    ua = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'}
    payload = {'q': searchfor}
    response = requests.get(link, headers=ua, params=payload)
    response_text = json.loads(response.text)
    results = response_text['responseData']['results']
    output = []
    for result in results[:min(3, len(results))]:
        output.append(strip_tag(result['title']).encode('utf-8'))
        output.append(result['url'])
    return output
