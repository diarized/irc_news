import feedparser

def parse_feeds(feeds):
    for feed in feeds:
        feed_name, feed_url = feed
        news = feedparser.parse(feed_url)
        for entry in news['entries']:
            entry['link'] = entry['link'].encode('ascii', 'ignore')
            entry['title'] = entry['title'].encode('ascii', 'ignore')
            title = entry['title'].strip()
            link = entry['link'].strip()
            yield (feed_name, title, link)
