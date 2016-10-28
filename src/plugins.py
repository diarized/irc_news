import lxml.html
import re
import duckduckgo
import rssfeed
import urlparse


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
    result = duckduckgo.get_zci(searchfor)
    return [result]


def rss(args):
    reload(rssfeed)
    url_parts = urlparse.urlparse(args[0])
    url = url_parts[0] + '://' + url_parts[1] + '/' + url_parts[2]
    feeder = rssfeed.RSSFeed('RSS feed', url)
    result = []
    for title, link in feeder.get_entries():
        if not title.startswith('/') and not link.startswith('/'):
            result.append(title)
            result.append('    ' + link)
    return result
