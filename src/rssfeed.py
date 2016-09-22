import feedparser

class RSSFeed(object):
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def _download(self):
        return feedparser.parse(self.url)

    def get_entries(self):
        content = self._download()
        encoded = []
        for entry in content['entries']:
            title = entry['title'].encode('ascii', 'ignore')
            link = entry['link'].encode('ascii', 'ignore')
            yield (title.strip(), link.strip())
