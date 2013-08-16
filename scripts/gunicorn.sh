#!/bin/sh
gunicorn --pythonpath ../inquizition inquizition:app -b '0.0.0.0:8000' -w 3 -D -p gunicorn.pid
