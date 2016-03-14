import pprint
import requests
import json

def help(*args, **kwargs):
    output = ["Use google search_string to get example functionlity of the system"]
    return output

def google(searchfor=''):
    if not len(searchfor):
        return ['']
    link = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&{}'.format(searchfor)
    ua = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'}
    payload = {'q': searchfor}
    response = requests.get(link, headers=ua, params=payload)
    response_text = json.loads(response.text)
    results = response_text['responseData']['results']
    pprint.pprint(results)
    output = []
    for result in results:
        output.append(result['titleNoFormatting'])
        output.append(result['url'])
    pprint.pprint(output)
    return output
