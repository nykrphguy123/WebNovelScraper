#!/usr/bin/python3.4

#I read a lot and I find it rather annoying that I have to manually copy and paste the text into notepad
#then save it as a file. Made this so I can just c&p the link and get the .txt with the contents easily.
#Really makes my life so much easier~!

import requests
import urllib.request
import re
import os
from tqdm import tqdm
from bs4 import BeautifulSoup

TGREEN = '\033[32m'
TPURPLE = '\033[35m'
TWHITE = '\033[37m'
TYELLOW = '\033[33m'

number_of_chapters = []
volume_number = []

num = 0
bad_chars = 'volume()'
translate_quotations = '“”'
replace_quotations = '""'

table=str.maketrans('','',bad_chars)
table2=str.maketrans(translate_quotations, replace_quotations)

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

title = soup.find('h2', {'class' : 'book_title'}).get_text()
chuu = soup.find('span', {'class' : 'total'})
yuh = str(chuu)
recent_volume = volume_number[0].translate(table)
volume_number_int = int(recent_volume)

os.system('clear')
print('Extracting ' + TYELLOW + yuh[20:24].translate(table) + TWHITE + ' chapters')
print('Novel: ' + TPURPLE + title + TWHITE)
print('\n')

for num in tqdm(range(volume_number_int)):
    num += 1
    link = 'https://novel.naver.com/best/detail.nhn?novelId=' + novel_ID + '&volumeNo=' + str(num)
    second_response = requests.get(link)
    soup2 = BeautifulSoup(second_response.text, 'html.parser')
    one_p_tag = soup2.findAll('p')[0].next
    story_exists = soup2.find("div", {"class":"detail_view_content ft15"})
    if story_exists != None:
        with open(title + '' + str(num) + '.txt', 'w') as text_file:
            chuu = re.sub(' +', ' ',str(one_p_tag))
            print(chuu.translate(table2), file=text_file)
    else:
        continue
        
print('\n')
print(TGREEN + 'Finished scraping ' + title + TWHITE)


#result = soup.find("div", {"class":"detail_view_content ft15"})

