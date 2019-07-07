#!/usr/bin/python3.4

#I read a lot and I find it rather annoying that I have to manually copy and paste the text into notepad
#then save it as a file. Made this so I can just c&p the link and get the .txt with the contents easily.
#Really makes my life so much easier~!

import requests
import urllib.request
import time
from bs4 import BeautifulSoup

print('input URL to webnovel')
novel = input()
url = novel

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
#soup = BeautifulSoup(response.text, "html.parser")

#soup.findAll('p')
#one_p_tag = soup.findAll('p')
one_p_tag = soup.findAll('p')[0].next

with open("Output.txt", "w") as text_file:
    print(one_p_tag, file=text_file)




