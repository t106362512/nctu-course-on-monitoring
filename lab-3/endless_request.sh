#! /bin/sh

set -x

while :
do
  curl http://localhost:8000/foo &
  curl http://localhost:8000/foo &
  curl http://localhost:8000/foo &

  curl http://localhost:8000/bar &
  
  sleep 1
done