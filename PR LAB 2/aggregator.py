import queue
from flask import Flask, request
import time
import threading
import producer

aggregator = Flask('aggregator')

producer_queue = queue.Queue(maxsize=10)
consumer_queue = queue.Queue(maxsize=10)


def run_aggregator():
    aggregator.run(host='127.0.0.1', port=8082)


@aggregator.get('/send')
def send():
    for ag in aggregator_generators:
        ag.start()
    for ae in aggregator_extractors:
        ae.start()

    return 'sending the data'


@aggregator.post('/aggregator/receive/from/consumer')
def consume():
    consumer_queue.put(request.form['value'])
    return ' '


@aggregator.post('/aggregator/receive/from/producer')
def receive_data_back():
    producer_queue.put(request.form['value'])
    return ' '


def send_consumer_aggregated_data(http):
    URL = 'http://127.0.0.1:8080/producer/receive/from/aggregator'
    while True:
        value = consumer_queue.get()
        http.request('POST', URL, fields={
            'value': value})
        time.sleep(1)


def send_producer_aggregated_data(http):
    URL = 'http://127.0.0.1:8081/consumer/receive/from/aggregator'
    while True:
        value = producer_queue.get()
        http.request('POST', URL, fields={
            'value': value})
        time.sleep(1)


aggregator_generators = [threading.Thread(target=send_producer_aggregated_data, args=(producer.http,))
                         for i in range(10)]
aggregator_extractors = [threading.Thread(target=send_consumer_aggregated_data, args=(producer.http,))
                         for i in range(5)]

if __name__ == '__main__':
    t_aggregator = threading.Thread(target=run_aggregator)
    t_aggregator.start()
