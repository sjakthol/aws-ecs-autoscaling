#!/usr/bin/env python3

import boto3
import logging
import os
import signal
import sys
import time
import uuid

def main():
    sqs = boto3.resource('sqs')
    queue_url = os.environ['QUEUE_URL']

    logging.info(f'Starting to produce messages to queue {queue_url}')
    queue = sqs.Queue(queue_url)

    last_report = time.time()
    sent = 0

    alive = True
    def stop(signal, __):
        logging.info(f'Received signal {signal}. Stopping producer.')
        nonlocal alive
        alive = False

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)

    while alive:
        entries = [{'Id': str(i), 'MessageBody': str(uuid.uuid4())} for i in range(3)]
        queue.send_messages(Entries=entries)

        sent += len(entries)

        diff = time.time() - last_report
        if diff > 2:
            logging.info(f'Sent {sent} messages in last {diff} seconds')
            last_report = time.time()
            sent = 0

        time.sleep(1)

    logging.info('Producer finished. Bye!')

if __name__ == '__main__':
    level = logging.DEBUG if '-v' in sys.argv else logging.INFO
    logging.basicConfig(level=level)

    main()