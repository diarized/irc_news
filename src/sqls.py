sql_list = {
        'search_link': "SELECT title, link FROM links WHERE link LIKE %s",
        'search_title': "SELECT title, link FROM links WHERE title LIKE %s",
        'add_link': "INSERT INTO links (title, link) VALUES (%s, %s)",
        'get_feeds': "SELECT name, url FROM feeds WHERE active = true",
}
