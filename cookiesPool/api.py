import json
from flask import Flask, g
from config import GENERATOR_MAP
from db import RedisClient

__all__ = ['app']

app = Flask(__name__)

@app.route('/')
def index():
    return '<h2>Welcome to Cookie Pool System</h2>'

def get_conn():
    for website in GENERATOR_MAP:
        if not hasattr(g, website):
            setattr(g, website + '_cookies', eval('RedisClient' + '("cookies", "' + website +'")'))
            setattr(g, website + '_accounts', eval('RedisClient' + '("accounts", "' + website +'")'))
    return g

@app.route('/<website>/random')
def random(website):
    g = get_conn()
    cookies = getattr(g, website + '_cookies').random()
    return cookies

@app.route('/<website>/count')
def count(website):
    g = get_conn()
    count = getattr(g, website + '_cookies').count()
    return json.dumps({'status': '1', 'count': count})

if __name__ == '__main__':
    app.run()