import lxml.html
import re
import duckduckgo
import rssfeed


def strip_tag(s):
    doc = lxml.html.fromstring(s)   # parse html string
    txt = doc.xpath('text()')       # ['foo ', ' bar']
    txt = ' '.join(txt)             # 'foo   bar'
    return re.sub('\s+', ' ', txt)  # 'foo bar'


def help(*args, **kwargs):
    output = ["Use `ddg ircbot` as an example"]
    return output


def google(searchfor=''):
    return ['Google search available only with Custom Search Engine API']


def ddg(query=None):
    searchfor = ' '.join(query)
    if not searchfor or not len(searchfor):
        return ['Search term not defined']
    try:
        result = duckduckgo.get_zci(searchfor)
    except ValueError:
        return ['Plugin found no results']
    return [result]


def rss(args):
    reload(rssfeed)
    url = args[0]
    try:
        max_entries = args[1]
        feeder = rssfeed.RSSFeed('RSS feed', url, max_entries)
    except IndexError:
        feeder = rssfeed.RSSFeed('RSS feed', url)
    result = []
    for title, link in feeder.get_entries():
        if not title.startswith('/') and not link.startswith('/'):
            result.append(title)
            result.append('    ' + link)
    return result
