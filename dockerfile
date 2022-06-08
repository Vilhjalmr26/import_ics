FROM python:3.9.13-alpine3.16


ENV ICS_URL="https://example.com/dav.php"
ENV ICS_USERNAME="username"
ENV ICS_PASSWORD="password"
ENV CRONTAB_SCHEDULE="0 0 * * *"
ENV TZ="UTC"

RUN apk update && apk add tzdata

COPY ./import_ics /import_ics
WORKDIR import_ics
RUN mkdir ical_export
RUN mkdir samples
RUN mv calendar_download_map.py samples/calendar_download_map.py

RUN mkdir /config
RUN ln -s /config/calendar_download_map.py calendar_download_map.py

RUN pip install -r requirements.txt

COPY ./import_ics.sh /import_ics.sh
RUN chmod 500 /import_ics.sh

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod 500 /entrypoint.sh
ENTRYPOINT /entrypoint.sh

