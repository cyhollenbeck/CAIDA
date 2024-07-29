#!/bin/bash
# Use the PORT environment variable if set, otherwise default to 8000
## /home/site/wwwroot/startup.sh  > /home/site/wwwroot/startuplog.log 2>&1
pwd > /home/site/wwwroot/startuplog.log 2>&1
pip install -r requirements.txt >> /home/site/wwwroot/startuplog.log 2>&1
PORT=${PORT:-8000} >> /home/site/wwwroot/startuplog.log 2>&1
exec gunicorn --bind 0.0.0.0:$PORT app:app >> /home/site/wwwroot/startuplog.log 2>&1