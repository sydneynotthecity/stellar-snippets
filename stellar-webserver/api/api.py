import flask
from flask import request, jsonify, abort
from flask_caching import Cache
from marshmallow import Schema, fields, validate
import datetime

config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config.from_mapping(config)
cache = Cache(app)

class SnippetsInputSchema(Schema):
    """ /snippets - POST

    Parameters:
     - name (str)
     - expires_in (int)
     - snippet (str)
    """
    # the 'required' argument ensures the field exists
    name = fields.Str(required=True)
    expires_in = fields.Int(required=True)
    snippet = fields.Str(required=True)

snippets_input_schema = SnippetsInputSchema()

@app.route('/snippets', methods=['POST'])
def save_snippet():
    # validate request data
    errors = snippets_input_schema.validate(request.json)
    if errors:
        abort(412, str(errors)) # BAD REQUEST

    body = request.json

    # build return body
    return_body = {}
    return_body['url'] = f"{request.base_url}/{body['name']}"
    return_body['name'] = body['name']
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=body['expires_in'])
    return_body['expires_at'] = expires_at.strftime("%Y-%m-%dT%H:%M:%SZ")
    return_body['snippet'] = body['snippet']

    # save snippet in cache
    cache.set(body['name'], return_body, timeout=body['expires_in'])
    return jsonify(return_body), 201

@cache.cached(timeout=30)
@app.route('/snippets/<name>', methods=['GET'])
def fetch_snippet(name):
    # if the cache has expired, return 404
    if not cache.get(name):
        return abort(404, 'URL Not Found')

    # get cache, extend timeout
    return_body = cache.get(name)
    new_time = datetime.datetime.strptime(return_body['expires_at'], '%Y-%m-%dT%H:%M:%SZ')
    extend_time = new_time + datetime.timedelta(seconds=30)
    return_body['expires_at'] = extend_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    cache.set(return_body['name'], return_body, timeout=30)
    return jsonify(return_body), 200

app.run()
