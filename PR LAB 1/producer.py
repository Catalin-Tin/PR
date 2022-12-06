from flask import Flask, request
import random
import time

producer = Flask('producer')


@producer.post('/receive')
def receive_data():
    print(request.form['value'])
    return ' '


def randomString():
    chrs = 'ABCDEFGHIJKLMNOPQRSTUVWYZ'
    return ''.join(random.choices(chrs, k=5))


def send_data(http):
    URL = 'http://127.0.0.1:8081/process'
    while True:
        http.request('POST', URL, fields={
            'value': randomString()})
        time.sleep(10)
