#!/usr/bin/env python

from flask import Flask, request, jsonify
import flask_restful as rest
import storage

app = Flask(__name__)
api = rest.Api(app)
db = storage.LinksDB()

parser = rest.reqparse.RequestParser()
parser.add_argument('link')
parser.add_argument('title')

class HelloWorld(rest.Resource):
    def get(this):
        return {'hello': 'world!'}

class LinksApi(rest.Resource):
    def post(this):
        args = parser.parse_args()
        link_pattern = args['link']
        rows = db.search_link(link_pattern)
        return jsonify(rows)

    def get(this, link_pattern):
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
    # app.run(debug=True, host='0.0.0.0', port=7777)

    api.add_resource(HelloWorld, '/')
    api.add_resource(LinksApi, '/api/v1.0/links', '/api/v1.0/links/<link_pattern>')
    app.run(debug=True, host='0.0.0.0', port=7777)
