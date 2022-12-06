from consumer import consumer, process_and_send_back
from producer import producer, send_data
import threading
import urllib3


def start_producer():
    producer.run(host='127.0.0.1', port=8080)


def start_consumer():
    consumer.run(host='127.0.0.1', port=8081)


@producer.get('/send')
def send():
    for g in generating:
        g.start()
    for e in extracting:
        e.start()
    return 'sending the data'


http = urllib3.PoolManager()

generating = [threading.Thread(target=send_data, args=(http,))
              for i in range(5)]
extracting = [threading.Thread(target=process_and_send_back, args=(http,))
              for i in range(4)]

if __name__ == '__main__':
    t_producer = threading.Thread(target=start_producer)
    t_consumer = threading.Thread(target=start_consumer)
    t_producer.start()
    t_consumer.start()
