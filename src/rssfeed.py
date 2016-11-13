import feedparser
import urlparse


class RSSFeed(object):
    def __init__(self, name, url, max_entries=12):
        self.name = name
        url_parts = urlparse.urlparse(url)
        self.url = url_parts[0] + '://' + url_parts[1] + '/' + url_parts[2]
        self.max_entries = int(max_entries)

    def _download(self):
        return feedparser.parse(self.url)

    def get_entries(self):
        content = self._download()
        max_posts = min([self.max_entries, len(content)])
        for entry in content['entries'][:max_posts]:
            title = entry['title'].encode('ascii', 'ignore')
            link = entry['link'].encode('ascii', 'ignore')
            yield (title.strip(), link.strip())
