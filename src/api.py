#!/usr/bin/env python

# Run me
# PYTHONPATH=/home/artur/Scripts/Python/src/irc_news/src ./api.py > /dev/null 2>&1 &

from flask import Flask, jsonify
import flask_restful as rest
import storage

db = None
parser = None


class HelloWorld(rest.Resource):
    def get(this):
        return {'hello': 'world!'}


class LinksSearchApi(rest.Resource):
    def post(this):
        args = parser.parse_args()
        link_pattern = args['link']
        rows = db.search_link(link_pattern)
        return jsonify(rows)

    def get(this, link_pattern):
        rows = db.search_link(link_pattern)
        return jsonify(rows)


class TitleSearchApi(rest.Resource):
    def post(this):
        args = parser.parse_args()
        title_pattern = args['title']
        rows = db.search_title(title_pattern)
        return jsonify(rows)

    def get(this, title_pattern):
        rows = db.search_title(title_pattern)
        return jsonify(rows)


class PostApi(rest.Resource):
    def post(this):
        args = parser.parse_args()
        title = args['title']
        link = args['link']
        added = db.add_link(title, link)
        if added:
            return 'Link added'
        return 'Adding a link failed.'

    def get(this):
        rest.abort(404, message="Method not allowed.")


def main():
    app = Flask(__name__)
    api = rest.Api(app)
    global db
    db = storage.LinksDB()

    global parser
    parser = rest.reqparse.RequestParser()
    parser.add_argument('link')
    parser.add_argument('title')

    api.add_resource(HelloWorld, '/')
    api.add_resource(LinksSearchApi, '/api/v1.0/links', '/api/v1.0/links/<link_pattern>')
    api.add_resource(TitleSearchApi, '/api/v1.0/titles', '/api/v1.0/titles/<title_pattern>')
    api.add_resource(PostApi, '/api/v1.0/add_link')
    return app


if __name__ == '__main__':
    app = main()
    app.run(debug=True, host='0.0.0.0', port=7777)
else:
    app = main()
