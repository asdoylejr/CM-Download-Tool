#! /usr/bin/python3

import os
import re
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, urlretrieve

# Directory we're getting busy in.
base_dir = os.cwd()

# Pass in CM file string to check date (signifying the version)
def check_cm_version(cmfile):
    date_check = re.compile(r'[0-9]{8}')
    return date_check.findall(cmfile)[0]

# Returns the latest version of CM from CM's download page.
# This function needs a lot of work.  It assumes way too much about the structure of
# the page and its consistency over time.
def pull_web_version(rom_url):
    available_files = []
    html_data = urlopen(rom_url)
    soup = bs(html_data)

    for links in soup.findAll(href = re.compile(r'\.zip$')):
        links = links.get("href")
        available_files.append(links)

    return available_files[0]

# Returns the version in my local directory.  This too needs work.  Right now
# the script just deletes the old version, but I'd like it to be able to handle
# having multiple versions in the directory.
def check_local_version():
    cm_file = None
    cur_dir = os.listdir()
    for files in cur_dir:
        if "cm-" in files:
            cm_file = files
    return cm_file

# Compares the web version and the local version and downloads the web version
# if it is newer.  I suppose this is fine for now.
def version_compare(localfile, webfile):
    local_version = int(check_cm_version(localfile))
    web_version = int(check_cm_version(webfile))

    if web_version > local_version:
        print("Downloading new file...")
        urlretrieve(webfile)
        print("Deleting old file...")
        os.remove(str(base_dir) + localfile)
    else:
        print("Latest version present...")

# Launch the script.
if __name__ == "__main__":

    base_url = "https://download.cyanogenmod.org/"
    device_tag = "d2lte"
    rom_url = base_url + "?device=" + device_tag
    web_version = pull_web_version(rom_url)
    local_version = check_local_version()
    version_compare(local_version, web_version)



