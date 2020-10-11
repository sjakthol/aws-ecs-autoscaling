#!/usr/bin/env python3

import boto3
import hashlib
import logging
import os
import signal
import sys
import time

def process_message(body):
    logging.debug(f'Received message: {body}')

    start = time.perf_counter()
    # First simulate some compute heavy workload
    h = hashlib.sha256()
    for _ in range(500000):
        h.update(body.encode('utf-8'))
    h.hexdigest()

    # Then, spend simulate network latency
    time.sleep(0.050)

    duration = time.perf_counter() - start
    logging.debug(f'Message processed in {duration} seconds')

def main():
    sqs = boto3.resource('sqs')
    queue_url = os.environ['QUEUE_URL']

    logging.info(f'Starting to consume {queue_url}')
    queue = sqs.Queue(queue_url)

    last_report = time.time()
    processed = 0

    alive = True
    def stop(signal, __):
        logging.info(f'Received signal {signal}. Stopping consumer.')
        nonlocal alive
        alive = False

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)

    while alive:
        messages = queue.receive_messages(MaxNumberOfMessages=10, VisibilityTimeout=60, WaitTimeSeconds=1)
        for message in messages:
            process_message(message.body)
            message.delete()

        processed += len(messages)

        diff = time.time() - last_report
        if diff > 10:
            logging.info(f'Processed {processed} messages in last {diff} seconds')
            last_report = time.time()
            processed = 0

    logging.info('Consumer finished. Bye!')

if __name__ == '__main__':
    level = logging.DEBUG if '-v' in sys.argv else logging.INFO
    logging.basicConfig(level=level)

    main()