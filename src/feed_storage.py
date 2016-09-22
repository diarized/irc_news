import irc
import threading
import logging
import time
import publishing
import config
import rssfeed
import sys

DEBUG = False  # True clears the database
REFRESH_TIME = 300

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s %(levelname)s] (%(threadName)-10s) %(message)s',
)


class FeedStorage(threading.Thread):
    def __init__(self):
        self.channel = "#999net"
        self.irc_thread = irc.IRCConnector([self.channel])
        time.sleep(5)
        self.channel_thread = self.irc_thread.channel_threads[self.channel]
        self.say = self.channel_thread.say
        super(FeedStorage, self).__init__(name='FeedStorage')

    def run(self):
        self.db = publishing.DbConnector()
        while not self.irc_thread.kill_received.is_set():
            if DEBUG:  # DEBUG clears table in database
                logging.debug('Clearing the database.')
            for entry in self.get_entries():
                self.publish_entry(entry)
            time.sleep(REFRESH_TIME)
        if self.conn:
            self.conn.close()
        if self.pconn:
            self.pconn.close()
        # self.irc_thread.join()
        # self.irc_thread.exit()
        sys.exit()

    def get_entries(self):
        feeds = config.get_feeds()
        for f in feeds:
            feed = rssfeed.RSSFeed(f[0], f[1])
            for entry in feed.get_entries():
                yield entry

    def publish_entry(self, entry):
        published = self.db.store_link(entry)
        if published:
            time.sleep(1)
            message = ' | '.join(entry)
            logging.debug('To IRC: ' + message)
            self.say(message)
            logging.info("I am FeedStorage after super (thread {})".format(
                threading.current_thread())
            )
            self.db.set_link_published(entry)
        else:
            logging.error('Link not stored and not published: ' + entry[0])
