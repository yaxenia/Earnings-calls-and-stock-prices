import pandas as pd
import numpy as np
import nltk
import string
import re
import os
import re
import time
import csv
import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import date, timedelta, datetime
from urllib.request import urlopen
import pandas as pd
import numpy as np
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import random
from time import sleep
from bs4 import BeautifulSoup

import requests

#donloading all urls



#api key
with open("api_key.txt", "r", encoding="utf-8") as f:
    api_key = f.read().strip()
#list of urls
with open("urls.txt", "r", encoding="utf-8") as f:
    urls = f.read().split("\n")

tickers = []
companys = []
titles = []
dates_ = []
times = []
quarters = []
company_info = []
Speech_table = []
qa_table = []
Comp_part = []
speech = []
speaker = []
qa_speech = []
qa_speaker = []
comp_parts = []
comp_pos = []
conf_parts = []
conf_pos = []
Conf_part = []
comp_conf_id = []
speech_conf_id = []
QA_conf_id = []
comppart_conf_id = []
confpart_conf_id = []
speech_script_id = []
QA_script_id = []
comppart_part_id = []
confpart_part_id = []
test_list = []

try:
    counter = company_info['CC ID'].iloc[-1] + 1
    counter_2 = qa_table['Script ID'].iloc[-1] + 1
    counter_3 = Conf_part['Part ID'].iloc[-1] + 1
except:
    counter = 0
    counter_2 = 0
    counter_3 = 0
for _, i in enumerate(urls):
    article_id = i.replace("https://seekingalpha.com/article/", "")[:7]
    retry = 5
    while retry > 0:

        url = "https://seeking-alpha.p.rapidapi.com/articles/get-details"

        querystring = {"id": article_id}

        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "seeking-alpha.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring).json()
        if response.get("data", None):
            break
        print(f"Retry {retry} {response}")
        retry -= 1
        sleep(1)
    if retry == 0:
        print(f"Skipped: {article_id}")
        continue
    sleep(1)
    #tracking progress
    if _ % 100 == 0:
        print(_, " ", article_id)
    else :
        print(article_id)
    soup = BeautifulSoup(response["data"]["attributes"]["content"], 'html.parser')
    #append all conferences
    test_list = []
    try:
        test = soup.find_all('p')
    except:
        print(soup)
    for c in test:
        #Append only conferences with earnings calls
        x = c.text.strip()
        test_list.append(x)
    if ('Operator' in test_list) and ('Company Participants' in test_list):
        # Company Info Section
        # Create conference_id
        cc_id = counter
        # Find company ticker
        try:
            ticker = soup.find('a').text.split(" ")[-1]
            tickers.append(ticker)
        except:
            tickers.append('None')
        # Find company name
        try:
            company = soup.find('a').text.split(" ")[0:-1]
            company = " ".join(company)
            companys.append(company)
        except:
            companys.append('None')
        # Find call title
        try:
            title = soup.find('h1').text
            titles.append(title)
        except:
            titles.append('None')
        # Find quarter/year
        try:
            date_text = soup.find('p').text.split(') ')[1]
            quarter = date_text[0:7]
            quarters.append(quarter)
        except:
            quarters.append('None')
        # Find call date
        try:
            date_string = date_text[date_text.index('Call') + 5:].split("Call ")[0]
            date = date_string[:date_string.index(":") - 2].strip()
            dates_.append(date)
        except:
            dates_.append('None')
        # Find call time
        try:
            time = date_string[date_string.index(":") - 2:].strip()
            times.append(time)
        except:
            times.append('None')
        # Add CC ID
        comp_conf_id.append(cc_id)
        # Speech and Company Participants Section
        bj = []
        indices = []
        convo = []
        # Pull speech script section
        script = soup.find_all('p')
        # pull strong tags from speech script section
        for i in script:
            if i.find('strong') is not None:
                g = "strong"
            else:
                g = 0
            bj.append(g)
        # Create list of index position of strong tags
        for j in range(len(bj)):
            if bj[j] == 'strong':
                indices.append(j)
        # Create list of text from speech script
        for k in script:
            x = k.text.strip()
            convo.append(x)
        # Create script ID & Participant ID
        script_id = counter_2
        part_id = counter_3
        # Create index objects to find positions of speech & participant sections
        try:
          conf_part_index = convo[convo.index('Conference Call Participants') + 1:convo.index('Operator')]
        except:
          conf_part_index = convo[convo.index('Company Participants') + 1:convo.index('Operator')]
        try:
            speech_index = indices[0:indices.index(convo.index('Question-and-Answer Session'))]
        except:
            speech_index = indices[0:indices.index(convo.index('Question-And-Answer Session'))]
        try:
            QA_index = indices[indices.index(convo.index('Question-and-Answer Session')) + 1:]
        except:
            QA_index = indices[indices.index(convo.index('Question-And-Answer Session')) + 1:]
        try:
            if article_id == 4420066 or article_id == "4420066":
              comp_part_index = 0
            else:
              comp_part_index = convo[convo.index('Company Participants') + 1:convo.index('Conference Call Participants')]
        except:
            comp_part_index = convo[
                              convo.index('Corporate Participants') + 1:convo.index('Conference Call Participants')]
        # Pulling info from speech section
        for i in range(2, len(speech_index) - 1):
            try:
                z = convo[speech_index[i] + 1:speech_index[i + 1]]
                speech.append(z)
            except:
                speech.append('None')
            try:
                g = convo[speech_index[i]]
                speaker.append(g)
            except:
                speaker.append('None')
            # Add CC ID & Script ID
            speech_conf_id.append(cc_id)
            speech_script_id.append(script_id)
        counter_2 += 1
        script_id = counter_2
        # Pulling info from Q&A section
        for i in range(0, len(QA_index) - 1):
            try:
                q = convo[QA_index[i] + 1:QA_index[i + 1]]
                qa_speech.append(q)
            except:
                qa_speech.append('None')
            try:
                f = convo[QA_index[i]]
                qa_speaker.append(f)
            except:
                qa_speaker.append('None')
            # Add CC ID & Script ID
            QA_conf_id.append(cc_id)
            QA_script_id.append(script_id)
        counter_2 += 1
        script_id = counter_2
        # Pulling company participants
        for i in comp_part_index:
            x = i.split('-')
            try:
                a = x[0]
                comp_parts.append(a)
            except:
                comp_parts.append('None')
            try:
                b = x[1]
                comp_pos.append(b)
            except:
                comp_pos.append('None')
            # Add CC ID & Part ID
            comppart_conf_id.append(cc_id)
            comppart_part_id.append(part_id)
            counter_3 += 1
            part_id = counter_3
        # Pulling conference participants
        for i in conf_part_index:
            x = i.split('-')
            try:
                a = x[0]
                conf_parts.append(a)
            except:
                conf_parts.append('None')
            try:
                b = x[1]
                conf_pos.append(b)
            except:
                conf_pos.append('None')
            # Add CC ID & Part ID
            confpart_conf_id.append(cc_id)
            confpart_part_id.append(part_id)
            counter_3 += 1
            part_id = counter_3
        # Add to CC ID
        counter += 1
# else:
# continue
# Pause in between trying each call transcript
sleep(random.randint(1, 2))
#Create company info table
company_info = pd.DataFrame({'CC ID':comp_conf_id, 'Tickers':tickers, 'Company':companys, 'Call Title':titles, 'Fiscal Quarter':quarters, 'Date':dates_, 'Time':times})
#Create Speech table
Speech_table = pd.DataFrame({'CC ID':speech_conf_id, 'Script ID':speech_script_id, 'Participant':speaker, 'Speech':speech, 'Section': 'Speech'})
#Create Q&A table
qa_table = pd.DataFrame({'CC ID':QA_conf_id, 'Script ID':QA_script_id, 'Participant':qa_speaker, 'Speech':qa_speech, 'Section': 'Q&A'})
#Create Company participant table
Comp_part = pd.DataFrame({'CC ID':comppart_conf_id, 'Part ID':comppart_part_id, 'Participant':comp_parts, 'Position':comp_pos, 'Organization': 'None', 'Participant Type': 'Internal'})
#Create Conference participant table
Conf_part = pd.DataFrame({'CC ID':confpart_conf_id, 'Part ID':confpart_part_id, 'Participant':conf_parts, 'Position': 'None', 'Organization':conf_pos, 'Participant Type': 'External'})




Speech_table.to_csv("/Users/kseniayakunina/se/Диплом/speech.csv")
company_info.to_csv("/Users/kseniayakunina/se/Диплом/company_info.csv")
qa_table.to_csv("/Users/kseniayakunina/se/Диплом/qa.csv")
Comp_part.to_csv("/Users/kseniayakunina/se/Диплом/comp_part.csv")
Conf_part.to_csv("/Users/kseniayakunina/se/Диплом/conf_part.csv")
