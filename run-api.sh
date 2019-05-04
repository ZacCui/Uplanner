#!/bin/sh
gunicorn run:app --daemon --log-file uplanner-api.log -w 4 -b localhost:5000
