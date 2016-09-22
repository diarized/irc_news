#!/usr/bin/env python

import psycopg2 as sql
from sqls import sql_list
import pprint


class LinksDB(object):
    def __init__(this, database='api', username='ircapi', password='JestemT77'):
        this.connection = sql.connect(
            database=database, user=username, password=password
        )
        this.cursor = this.connection.cursor()

    def execute(this, sql_name, args=None):
        try:
            sql_command = sql_list[sql_name]
            this.cursor.execute(sql_command, args)
        except sql.InternalError:
            args_string = pprint.pformat(args)
            print("args = ", args_string)
            this.connection.rollback()
            raise
        return this.cursor.fetchall()

    def search_link(this, link_word):
        args = ('%' + link_word + '%',)
        links = this.execute('search_link', args)
        return links

    def search_title(this, title_word):
        args = ('%' + title_word + '%',)
        titles = this.execute('search_title', args)
        return titles

    def add_link(this, title, link):
        args = (title, link)
        confirmation = this.execute('add_link', args)
        return confirmation

    def get_feeds(this):
        feeds = this.execute('get_feeds')
        return feeds


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
