#!/bin/bash
# Use the PORT environment variable if set, otherwise default to 8000
## /home/startup/startup.sh > /home/site/wwwroot/startuplog.log 2>&1
PORT=${PORT:-8000}
exec gunicorn --bind 0.0.0.0:$PORT app:app