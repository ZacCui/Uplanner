#!/bin/sh
gunicorn run:app --log-file uplanner-api.log -w 4 -b localhost:5000
