import lxml.html
import re
import duckduckgo
import pprint


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
    result = duckduckgo.query(searchfor)
    for key in [result.definition, result.abstract, result.answer]:
        try:
            answer = key.text
            if answer and len(answer):
                pprint.pprint(answer)
                return [answer]
        except TypeError:
            pass
    return ['No results for "{}"'.format(searchfor)]
