import queue
from flask import Flask, request
import time


consumer = Flask('consumer')

queue = queue.Queue(maxsize=6)


@consumer.post('/process')
def process():
    queue.put(request.form['value'])
    return ' '


def process_and_send_back(http):
    URL = 'http://127.0.0.1:8080/receive'
    while True:
        value = queue.get()
        http.request('POST', URL, fields={
            'value': value})
        time.sleep(1)