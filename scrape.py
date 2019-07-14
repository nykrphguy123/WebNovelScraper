#!/usr/bin/python3.4

#I read a lot and I find it rather annoying that I have to manually copy and paste the text into notepad
#then save it as a file. Made this so I can just c&p the link and get the .txt with the contents easily.
#Really makes my life so much easier~!

import requests
import urllib.request
import time
import re
import os
from bs4 import BeautifulSoup

number_of_chapters = []
volume_number = []

num = 0
bad_chars = 'volume'
table=str.maketrans('','',bad_chars)

os.system('clear')

print('Enter URL to novel')
novel = input()
full_link = novel

novel_ID = full_link[46:]
response = requests.get(full_link)

soup = BeautifulSoup(response.text, "html.parser")

for link in soup.findAll('li'):
    number_of_chapters.append(link.get('id'))

for value in number_of_chapters:
    if value != None:
        volume_number.append(value)

number_of_chapters = len(volume_number)
recent_volume = volume_number[0].translate(table)
volume_number_int = int(recent_volume)

os.system('clear')
print('Fetching ' + str(number_of_chapters) + ' chapters..')
print('Novel ID: ' + novel_ID)

while num < volume_number_int+1:
    num += 1
    link = 'https://novel.naver.com/best/detail.nhn?novelId=' + novel_ID + '&volumeNo=' + str(num)
    second_response = requests.get(link)
    soup2 = BeautifulSoup(second_response.text, 'html.parser')
    one_p_tag = soup2.findAll('p')[0].next
    with open('webnovel'+ str(num) + '.txt', 'w') as text_file:
        print(one_p_tag, file=text_file)

os.system('clear')
print('Scraped ' + str(number_of_chapters) + ' chapters!')
