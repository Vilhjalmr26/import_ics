#!/usr/local/bin/python

import caldav
import pprint
import os
import requests

import calendar_download_map

class Import_ICS():
    def __init__(self): #, url, username, password, calendars = []):

        self.url = os.getenv('ICS_URL')
        self.username = os.getenv('ICS_USERNAME')
        self.password = os.getenv('ICS_PASSWORD')

        self.header = []
        self.events = []
        self.footer = ["END:VEVENT\n","END:VCALENDAR\n"]
        self.target_calendars = self.get_target_calendars()


    def reset_values(self):
        self.header = []
        self.events = []


    def get_target_calendars(self):
        self.download_calendars()
        filenames = []
        for filename in os.listdir("./ical_export"):
            if filename.endswith(".ics"):
                filenames.append(filename[:-4])
        pprint.pprint(filenames)
        return filenames

    def get_calendar_names(self):
        names = []
        with caldav.DAVClient(url=self.url, username=self.username, password=self.password) as client:
            my_principal = client.principal()
            calendars = my_principal.calendars()
            for cal in calendars:
                names.append(cal.name)
        return names

    def import_ics(self):
        with caldav.DAVClient(url=self.url, username=self.username, password=self.password) as client:
            my_principal = client.principal()
            calendars = my_principal.calendars()

            for cal in calendars:
                self.reset_values()
                if cal.name in self.target_calendars:
                    self.parse(cal.name)
                for event in self.events:
                    temp_event = "".join(self.header + event + self.footer)
                    cal.save_event(ical=temp_event)


    def create_new(self):
        avail_cals = self.get_calendar_names()
        for tar_cal in self.target_calendars:
            if tar_cal not in avail_cals:
                print("creating: " + tar_cal)
                with caldav.DAVClient(url=self.url, username=self.username, password=self.password) as client:
                    my_principal = client.principal()
                    my_principal.make_calendar(name=tar_cal)

    def parse(self, calendar_name):
        calendar_lines = []
        filename = "./ical_export/" + calendar_name + ".ics"
        with open(filename, 'r') as calendar_data:
            calendar_lines = calendar_data.readlines()

        mode = "header"
        temp_event = []
        for line in calendar_lines:
            if line.startswith("BEGIN:VEVENT"):
                mode = "events"
                temp_event = []
            elif (mode == "header") and (not line.startswith("METHOD")):
                self.header.append(line)
            elif line.startswith("END:VEVENT"):
                self.events.append(temp_event)
            elif not line.startswith("END:VCALENDAR"):
                temp_event.append(line)
        self.header.append("BEGIN:VEVENT\n")

    def download_calendars(self):
        for name, url in calendar_download_map.mapping.items():
            with open("./ical_export/" + name + ".ics", "wb") as outfile:
                response = requests.get(url)
                outfile.write(response.content)

if __name__=="__main__":
    icsImporter = Import_ICS()

    icsImporter.create_new()
    icsImporter.import_ics()

