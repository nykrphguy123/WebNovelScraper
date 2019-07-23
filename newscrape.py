#!/usr/bin/python3.4

#I read a lot and I find it rather annoying that I have to manually copy and paste the text into notepad
#then save it as a file. Made this so I can just c&p the link and get the .txt with the contents easily.
#Really makes my life so much easier~!

import requests
import urllib.request
import re
import os
import pprint
from tqdm import tqdm
from bs4 import BeautifulSoup

TGREEN = '\033[32m'
TPURPLE = '\033[35m'
TWHITE = '\033[37m'
TYELLOW = '\033[33m'

volume_number = []
chuu_number = []
pages = []
pagenum_cut = []

first_page = 1
translate_quotations = '“”'
replace_quotations = '""'

table2=str.maketrans(translate_quotations, replace_quotations)

os.system('clear')

#This gets the URL of the novel and gets the novel ID with string manipulation
print('Enter URL to novel')
novel = input()
full_link = novel
#print('Whats the last page of the novel?')
#last_page = int(input())

novel_ID = full_link[46:]

os.system('clear')

print(TYELLOW + 'Gathering volumes..' + TWHITE)

#This bit here finds the last page of the novel
last_page_link = 'https://novel.naver.com/best/list.nhn?novelId=' + novel_ID + '&page=' + '150'
response0 = requests.get(last_page_link)
soup0 = BeautifulSoup(response0.text, 'html.parser')
last_number = soup0.find('div', {'class' : 'paging NE=a:lst'})

for i in last_number.findAll('a'):
    pages.append(i.get('href'))

for j in pages:
    lp = j[35:]
    pagenum_cut.append(lp)

pagenum_cut.reverse()
findlastnum = pagenum_cut[0]

last_page_int = int(findlastnum)
last_page = last_page_int + 1

#Here we go through each page of the novel to get the list of links of each chapter
while first_page < last_page+1:
    link = 'https://novel.naver.com/best/list.nhn?novelId=' + novel_ID + '&page=' + str(first_page)
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    yuh = soup.find('ul', {'class' : 'list_type2 v3 league_num NE=a:lst'})
    for a in yuh.findAll('a'):
        volume_number.append(a.get('href'))
    first_page = first_page + 1

title_of_novel = soup.find('h2', {'class' : 'book_title'}).get_text()

#Remember those links that we got in that list? Lets iterate through it and use string manipulation to
#grab the chapter number of the novel by itself and store it in a list called chuu_number
for link in volume_number:
    vol_num = link[41:]
    chuu_number.append(vol_num)

volumes = len(chuu_number)

os.system('clear')

print('Extracting ' + TYELLOW + str(volumes) + TWHITE + ' volumes')
print('Novel: ' + TPURPLE + title_of_novel + TWHITE)

#The novel_link serves as a mold so we can just place the novel ID and the chapter. After that we'll
#iterate through each chapter in the list 'chuu_number' and scrape the first paragraph and save it
#as a text file
for num in tqdm(chuu_number):
    novel_link = 'https://novel.naver.com/best/detail.nhn?novelId=' + novel_ID + '&volumeNo=' + num
    response2 = requests.get(novel_link)
    soup2 = BeautifulSoup(response2.text, 'html.parser')
    title = soup2.find('a', {'class' : 'tit_book N=a:flt.end'}).get_text()
    one_p_tag = soup2.findAll('p')[0].next
    with open(title + ' ' + num + '.txt', 'w') as text_file:
        chuu = re.sub(' +', ' ',one_p_tag)
        print(chuu.translate(table2), file=text_file)

print('\n')
print(TWHITE + 'Finished scraping ' + TPURPLE + title + TWHITE)

