FROM python:3.10-alpine3.16

COPY requirements.txt /tmp/
COPY main.py /app

RUN apk add --no-cache --virtual .build-deps gcc libc-dev make g++ \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && apk del .build-deps gcc libc-dev make g++

WORKDIR /app/

ENV PYTHONPATH=/app

CMD ["python", "main.py"]
