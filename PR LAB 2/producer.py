from flask import Flask, request
import random
import time
import threading
import urllib3

producer = Flask('producer')
http = urllib3.PoolManager()


def start_producer():
    producer.run(host='127.0.0.1', port=8080)


@producer.post('/producer/receive/from/aggregator')
def receive_data():
    print(request.form['value'])
    return ' '


@producer.get('/send')
def sendProducer():
    for g in generating:
        g.start()
    return 'sending the data'


def randomString():
    chrs = 'ABCDEFGHIJKLMNOPQRSTUVWYZ'
    return ''.join(random.choices(chrs, k=5))


def send_producer_data(http):
    URL = 'http://127.0.0.1:8082/aggregator/receive/from/producer'
    while True:
        http.request('POST', URL, fields={
            'value': randomString()})
        time.sleep(5)


generating = [threading.Thread(target=send_producer_data, args=(http,))
              for i in range(10)]

if __name__ == '__main__':
    t_producer = threading.Thread(target=start_producer)
    t_producer.start()
