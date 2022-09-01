from python:3.10-alpine-3.16

COPY requirements.txt /tmp/
COPY main.py /app

RUN apk add --no-cache --virtual .build-deps gcc libc-dev make \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && apk del .build-deps gcc libc-dev make

WORKDIR /app/

ENV PYTHONPATH=/app

CMD ['python', 'main.py']
