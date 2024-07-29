###/home/startup/startup.sh
cp /home/default /etc/nginx/sites-enabled/default
service nginx restart

# install & start crontab
apt-get update --allow-releaseinfo-change && apt-get install cron -yqq
(crontab -l 2>/dev/null; echo "* * * * * (crontab -l) >> /home/site/wwwroot/cronresult.txt 2>&1")|crontab
(crontab -l 2>/dev/null; echo "@hourly (date)> /home/site/wwwroot/cronresult.txt")|crontab
(crontab -l 2>/dev/null; echo "* * * * * /usr/local/bin/php /home/site/wwwroot/artisan schedule:run >> /home/site/wwwroot/cronartisan.txt 2>&1")|crontab
(crontab -l 2>/dev/null; echo "@hourly (date) > /home/site/wwwroot/cronartisan.txt")|crontab
service cron start
