#!/usr/bin/env python

import feedparser
import storage


def get_feeds():
    db = storage.LinksDB()
    feeds = db.get_feeds()
    return feeds


def parse_feeds():
    feeds = get_feeds()
    for feed in feeds:
        feed_name, feed_url = feed
        news = feedparser.parse(feed_url)
        for entry in news['entries']:
            entry['link'] = entry['link'].encode('ascii', 'ignore')
            entry['title'] = entry['title'].encode('ascii', 'ignore')
            title = entry['title'].strip()
            link = entry['link'].strip()
            yield (feed_name, title, link)


if __name__ == '__main__':
    import pprint
    for feed in get_feeds():
        pprint.pprint(feed)
    for source, title, link in parse_feeds():
        pprint.pprint((source, title, link))
