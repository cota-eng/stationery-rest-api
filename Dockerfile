FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
# for db 
# RUN apk add --update --no-cache postgresql-client jpeg-dev
# RUN apk add --update --no-cache --virtual .tmp-build-deps \
#     gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

# stackoverflow
# RUN apk add gcc
# RUN apk add --no-cache libressl-dev musl-dev libffi-dev
# RUN pip install --no-cache-dir cryptography==2.1.4
# RUN apk del libressl-dev \
#         musl-dev \
#         libffi-dev

RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

# for db
# RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
# RUN adduser -D user
# RUN chown -R user:user /vol
# RUN chmod -R 755 /vol/web

# USER user
