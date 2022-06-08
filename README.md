# import_ics
Imports ICS files into a CalDAV server

Runs a python script at a crontab defined interval that downloads/imports ics files into a caldav server.

Environment Variables:
ICS_USERNAME - Username for caldav server
ICS_PASSWORD - Password for caldav server
ICS_URL - URL to the caldav server
CRONTAB_SCHEDULE - crontab time string, eg. "0 0 * * *"
TZ - Timezone eg. "America/Chicago"

creates a calendar_download_map.py file in the config path.  The dictionary contained within uses calendar name as key, and URL to ics as value.
Will download the ics file at the given URL and load its contents into the given calendar name, creating it if it doesnt exist.

If ics file is not from a download, you can put the file in the /config/ical_export forlder with calendar_name.ics as the filename.
Again, when run the script will import the ics file into  calendar_name, creating it if it doesnt exist.
