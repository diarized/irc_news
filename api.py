#!/usr/bin/env python

from flask import Flask, request, jsonify
import storage
import requests

app = Flask(__name__)
db = storage.LinksDB()

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/api/v1.0/links', methods=['POST'])
@app.route('/api/v1.0/links/<link_pattern>', methods=['GET'])
def search_link(link_pattern=None):
    if request.method == 'POST':
        link_pattern = request.form['link']
    rows = db.search_link(link_pattern)
    return jsonify(rows)

@app.route('/api/v1.0/titles', methods=['POST'])
@app.route('/api/v1.0/titles/<title_pattern>', methods=['GET'])
def search_title(title_pattern=None):
    if request.method == 'POST':
        title_pattern = request.form['title']
    rows = db.search_title(title_pattern)
    return jsonify(rows)

@app.route('/api/v1.0/add_link', methods=['POST'])
def post_link():
    title = request.form['title']
    link = request.form['link']
    added = db.add_link(title, link)
    if added:
        return 'Link added'
    return 'Adding a link failed.'

if __name__ == '__main__':
    # Test at http://cheap.stonith.pl:7777/api/v1.0/links/microsoft
    app.run(debug=True, host='0.0.0.0', port=7777)
