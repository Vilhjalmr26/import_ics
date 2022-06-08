#!/bin/sh

if ! [ -f "/config/calendar_download_map.py" ];
then
    cp /import_ics/samples/calendar_download_map.py /config/calendar_download_map.py
    chmod 777 /config/calendar_download_map.py
fi

cd /import_ics
echo "${CRONTAB_SCHEDULE} /import_ics.sh" > crontab

chown root:root /ical_export

crontab crontab

crond -f