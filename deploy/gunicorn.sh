#!/bin/bash

NAME='pos'
DJANGODIR=$(dirname $(cd `dirname $0` && pwd))
SOCKFILE=/tmp/gunicorn-pos.sock
LOGDIR=${DJANGODIR}/logs/gunicorn.log
NUM_WORKERS=4
DJANGO_WSGI_MODULE=config.wsgi

rm -frv $SOCKFILE

echo $DJANGODIR

cd $DJANGODIR

exec ${DJANGODIR}/env/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=$LOGDIR
