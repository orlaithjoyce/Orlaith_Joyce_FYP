# To retrieve the text for each contents url

#!/usr/local/bin/python

import os.path, random
import requests
from bs4 import BeautifulSoup
import urllib.request
import glob
import time

# Using html files in 'Contents' folder
# 1. Extract all speeches - Responses to questions
allfiles = glob.glob('./Data/Contents/Contents-*.html')
debate_speeches = []

for f in allfiles[0:5]: # test on subset of files
    print("Processing %s" % f)
    # Parse the full HTML file
    file_open = open(f, 'r')
    soup = BeautifulSoup(file_open, 'html.parser')

    results1 = soup.find_all("div",{"class":"db-section"})
    for tag1 in results1:
        results2 = tag1.find_all("div", {"class":"speech"}, recursive=True)
        # Process each speech
        for tag2 in results2:
            # Get speaker name
            speaker = None
            results3a = tag2.find_all("a", {"class":"c-avatar__name-link"})
            if not ( results3a is None or len(results3a) == 0 ):
                speaker = results3a[0].text.strip()
            # Get the paragraph text for each speech
            paragraphs = []
            results3b = tag2.find_all("p")
            for tag3b in results3b:
                paragraph = tag3b.text
                if not paragraph is None:
                    paragraphs.append( paragraph.strip() )
            if len(paragraphs) > 0:
                debate_speeches.append( (speaker, "\n".join( paragraphs ) ) )
    print("Found %d speeches" % len(debate_speeches) )

    # 2. Save each debate speech to a txt file (speaker name + speech text)
        # Name each file with the date_number in content file name
        # (e.g): use '2015-01-27_20' in ./Data/Contents/Contents-2015-01-27_20.html
        # Include an incrementing number in filename as there may be multiple 'speeches'
    num = 0
    for i in debate_speeches:
        num+=1
        filepath = "./Data/Speeches/Speech-{}.txt".format(f[25:-5] + "-" + str(num))
        print("Checking for %s" % filepath)
        # Check if file has already been downloaded
        if not os.path.exists( filepath ):
            print("Writing %s" % filepath)
            speech_out = open(filepath, "w")
            speech_out.write("%s\n\n" % i[0] )
            speech_out.write("%s\n" % i[1] )
            speech_out.close()
           
