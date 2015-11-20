#!/usr/bin/env python

import psycopg2 as sql

class LinksDB(object):
    def __init__(this, database='api', username='ircapi', password='JestemT77'):
        this.connection = sql.connect(database=database, user=username, password=password)
        this.cursor = this.connection.cursor()

    def search_link(this, link_word):
        try:
            this.cursor.execute("SELECT title, link FROM links WHERE link LIKE %s", ('%' + link_word + '%',))
        except sql.InternalError:
            print("link_word = ", link_word)
            this.connection.rollback()
            raise
        return this.cursor.fetchall()

    def search_title(this, title_word):
        try:
            this.cursor.execute("SELECT title, link FROM links WHERE link LIKE %s", ('%' + title_word + '%',))
        except sql.InternalError:
            print("title_word = ", title_word)
            this.connection.rollback()
            raise
        return this.cursor.fetchall()

    def add_link(this, title, link):
        try:
            this.cursor.execute("INSERT INTO links (title, link) VALUES (%s, %s)", (title, link))
        except sql.ProgrammingError:
            this.connection.rollback()
            raise
            return False
        else:
            this.connection.commit()
        return True

    def get_feeds(this):
        try:
            this.cursor.execute("SELECT name, url FROM feeds WHERE active = true")
        except sql.InternalError:
            this.connection.rollback()
            raise
        return this.cursor.fetchall()


if __name__ == '__main__':
    import requests
    # import pprint
    # db = LinksDB()
    # print(db.cursor)
    # pprint.pprint(db.search_link('onion'))
    # db_add_url = 'http://localhost:7777/api/v1.0/add_link'
    # test_values = {
    #         'title': 'I Am Sam',
    #         'link': 'http://localhost:7777/'
    # }
    # r = requests.post(db_add_url, test_values)
    # print r.text
    db_get_link_url = 'http://localhost:7777/api/v1.0/links'
    test_values = {'link': 'localhost'}
    r = requests.post(db_get_link_url, test_values)
    print r.text
    # db.connection.close()
