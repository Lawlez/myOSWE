## clean temp files older than 30 days
find /tmp -type f -mtime +30 -exec rm {} \;
find /var/tmp -type f -mtime +30 -exec rm {} \;

## optional delete temp backup files:

rm -rf /usr/local/psa/PMM/tmp/*

## optional delete other temp files:
rm -rf /usr/local/psa/tmp/*
