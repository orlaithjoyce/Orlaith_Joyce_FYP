# To get the URLs for the contents of each debate

#!/usr/local/bin/python

import os.path, random
import requests
from bs4 import BeautifulSoup
import urllib.request
import glob
import time

# Using html files in 'Debates' folder
allfiles = glob.glob('./Data/Debates/Debate-*.html')
site_prefix = "https://www.oireachtas.ie"
contents_links = []

for f in allfiles[0:5]: # test on subset of files
    print("Processing %s" % f)
    # Parse the full HTML file
    file_open = open(f, 'r')
    soup = BeautifulSoup(file_open, 'html.parser')

    # Find the nested pattern div -> li -> a
    results1 = soup.find_all("div", {"class":"results"})
    for tag1 in results1:
        results2 = tag1.find_all("li")
        for tag2 in results2:
            results3 = tag2. find_all("a")
            for tag3 in results3:
                link = tag3.get("href", "")
                # Check the link
                if link.startswith("/"):
                    # Create the full link
                    link = site_prefix + link
                    link = link.split("#")
                    link = link[0]
                    contents_links.append(link)
                    for link in contents_links:
                        # Save as html file
                        # Split URL by '/' to get the date and content number for that date
                        # https://www.oireachtas.ie/en/debates/debate/dail/2018-10-04/16/
                        x = link.split('/')
                        filepath = "Data/Contents/Contents-{}.html".format(x[7] + "_" + x[8])
                        print("Checking for %s" % filepath)
                        # Check if file has file already been downloaded
                        if not os.path.exists(filepath):
                            print("Fetching %s" % link)
                            lines = requests.get(link)
                            data = lines.text
                            fout = open(filepath, "w")
                            fout.write(data)
                            fout.close()
                            print("Wrote %s" % filepath )
                            time.sleep( random.randint(3,10) )