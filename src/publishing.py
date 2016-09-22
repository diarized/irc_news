import logging
import sqlite3 as sql
import psycopg2 as psql
import threading

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s %(levelname)s] (%(threadName)-10s) %(message)s',
)


class DbConnector(object):
    def __init__(self):
        logging.info("I am DBConnector (thread {})".format(
            threading.current_thread())
        )
        self.conn = sql.connect('hyrss')
        if not self.conn:
            logging.error('Sqlite3 db file disappeared or locked.')
            self.exit(1)
        logging.debug('conn is {0}'.format(self.conn))
        self.pconn = psql.connect(
            database='api', user='ircapi', password='JestemT77'
        )
        self.pconn.autocommit = True
        self.cursor = self.pconn.cursor()

    def store_link(self, entry):
        title = entry[0]
        link = entry[1]
        logging.debug('Storing link ' + title)
        try:
            self.conn.execute(
                "INSERT INTO rss VALUES('%s', '%s', '%s');" % (title, link, 0)
            )
            self.conn.commit()
            self.cursor.execute(
                "INSERT INTO links (title, link, published) VALUES(%s, %s, %s);",
                (title, link, False)
            )
        except (sql.OperationalError, sql.ProgrammingError, sql.IntegrityError), e:
            logging.error('Storing link failed: ' + title)
            print(e)
            return False
        except:
            raise
        else:
            return True

    def set_link_published(self, entry):
        title = entry[0]
        logging.debug(u'Link on IRC, setting it as published in database. ({0})'.format(title))
        try:
            self.conn.execute("UPDATE rss SET published = 1 WHERE title = '%s';" % title)
            self.conn.commit()
            self.cursor.execute("UPDATE links SET published = %s WHERE title = %s;", (True, title))
        except (sql.OperationalError, sql.ProgrammingError), e:
            logging.error('Setting link as published failed: ' + title)
            print e
            return False
        except:
            raise
        else:
            return True

    def clear_table(conn):
        logging.debug('DELETE FROM rss')
        conn.execute("DELETE FROM rss;")
        conn.commit()
