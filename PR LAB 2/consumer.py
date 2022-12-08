import queue
from flask import Flask, request
import time
import threading
import producer

consumer = Flask('consumer')

queue = queue.Queue(maxsize=6)


def start_consumer():
    consumer.run(host='127.0.0.1', port=8081)


@consumer.post('/consumer/receive/from/aggregator')
def process():
    queue.put(request.form['value'])
    return ' '


@consumer.get('/send')
def send():
    for e in extracting:
        e.start()

    return 'sending the data'


def send_consumer_data(http):
    URL = 'http://127.0.0.1:8082/aggregator/receive/from/consumer'
    while True:
        value = queue.get()
        http.request('POST', URL, fields={
            'value': value})
        time.sleep(1)


extracting = [threading.Thread(target=send_consumer_data, args=(producer.http,))
              for i in range(5)]

if __name__ == '__main__':
    t_consumer = threading.Thread(target=start_consumer)
    t_consumer.start()
