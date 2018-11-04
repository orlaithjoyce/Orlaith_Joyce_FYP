# To get the url for each debate

#!/usr/local/bin/python

import os.path, random
import requests
from bs4 import BeautifulSoup
import urllib.request
import glob
import time

# 1. Get the Pages with 100 debate urls
# Get the urls by changing the 'page= ' number. There are 82 pages to retrieve.
for i in range(1,83):
    url = "https://www.oireachtas.ie/en/debates/find/?page="+str(i)+"&datePeriod=all&debateType=dail&resultsPerPage=100"
    # Save each url as a html file
    filepath = "Data/Debates_100_per_page/%03d.html"% i
    print("Checking for %s" % filepath)
    # Check if file has already been downloaded
    if not os.path.exists( filepath ):
        print("Fetching %s" % url)
        lines = requests.get(url)
        data = lines.text
        fout = open(filepath, "w")
        fout.write(data)
        fout.close()
        print("Wrote %s" % filepath )
        time.sleep( random.randint(3,10) )

# 2. Get the debate urls on each of the pages saved above
# Using html files in 'Debates_100_per_page' folder
allfiles = glob.glob('./Data/Debates_100_per_page/*.html')
site_prefix = "https://www.oireachtas.ie"
debate_links = []

for f in allfiles[0:5]: # test on subset of files
        print("Processing %s" % f)
        # Parse the full HTML file
        file_open = open(f,'r')
        soup = BeautifulSoup(file_open, 'html.parser')
        #file_open.close()

        results1 = soup.find_all("div", {"class":"c-debates-expanding-list__item"})
        for tag1 in results1:
                results2 = tag1.find_all("a", {"class":"u-btn-secondary c-debates-expanding-list__button"})
                for tag2 in results2:
                        link = tag2.get("href", "")
                        # Check the link
                        if link.startswith("/"):
                                # Create the full link
                                link = site_prefix + link
                                debate_links.append(link)               
                                for link in debate_links:
                                        # Save as html file, use date of debate in file name
                                        filepath2 = "Data/Debates/Debate-{}.html".format(link[49:59])
                                        print("Checking for %s" % filepath2)
                                        # Check if file has already been downloaded
                                        if not os.path.exists( filepath2 ):
                                                print("Fetching %s" % link)
                                                lines2 = requests.get(link)
                                                data2 = lines2.text
                                                fout2 = open(filepath2, "w")
                                                fout2.write(data2)
                                                fout2.close()
                                                print("Wrote %s" % filepath2 )
                                                time.sleep( random.randint(3,10) )