#!/usr/bin/env python
# encoding: utf-8
from configparser import ConfigParser
import requests
from flask import jsonify
from flask import request
from flask import Flask
from flask import render_template
import time


app = Flask(__name__)
app.jinja_env.variable_start_string = '{['
app.jinja_env.variable_end_string = ']}'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/weather', methods=['GET'])
def getWeather():
    conf = config()
    city = request.args.get('city')
    city = city.lower()
    cities = [i[0] for i in conf.items('cities')]
    if(city in cities):
        query = {'q': city, 'appid': conf.get('weather', 'key')}
        resp = requests.get(
            url="https://api.openweathermap.org/data/2.5/weather", params=query)
        data = resp.json()
        data['updated_at'] = time.asctime(time.localtime(time.time()))
        return jsonify(data), 200
    else:
        data = {'error': 'the city not found'}
    return jsonify(data), 422


def config():
    conf = ConfigParser(allow_no_value=True)
    conf.read('./config.ini')
    return conf


if __name__ == '__main__':
    conf = config()
    app.run(host=conf.get('server', 'host'),
            port=conf.get('server', 'port'))
