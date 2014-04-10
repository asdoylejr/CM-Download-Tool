#! /usr/bin/python3

import os
import re
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, urlretrieve

# Pass in CM file string to check date (signifying the version)
def check_cm_version(cmfile):
    date_check = re.compile(r'[0-9]{8}')
    return date_check.findall(cmfile)[0]

def pull_web_version(rom_url):
    available_files = []
    html_data = urlopen(rom_url)
    soup = bs(html_data)

    for links in soup.findAll(href = re.compile(r'\.zip$')):
        links = links.get("href")
        available_files.append(links)

    return available_files[0]

def check_local_version():
    cm_file = None
    cur_dir = os.listdir()
    for files in cur_dir:
        if "cm-" in files:
            cm_file = files
    return cm_file

def version_compare(localfile, webfile):
    local_version = int(check_cm_version(localfile))
    web_version = int(check_cm_version(webfile))

    if web_version > local_version:
        print("Downloading new file...")
    else:
        print("Latest version present...")

# Launch script
if __name__ == "__main__":

    base_url = "https://download.cyanogenmod.org/"
    device_tag = "d2lte"
    rom_url = base_url + "?device=" + device_tag
    web_version = pull_web_version(rom_url)
    local_version = check_local_version()
    version_compare(local_version, web_version)



