FROM python:3.7-alpine

RUN python3 -m pip install --no-cache-dir boto3

RUN mkdir /app && chown nobody:nobody /app
WORKDIR /app
ADD --chown=nobody:nobody consumer.py /app

USER nobody
CMD ["python3", "consumer.py"]