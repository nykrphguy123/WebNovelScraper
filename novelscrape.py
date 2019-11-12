#!/usr/bin/python3.4

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
chapter_number = []
pages = []
pagenum_cut = []

pagenumber = 0
first_page = 1
translate_quotations = '“”'
replace_quotations = '""'

table2=str.maketrans(translate_quotations, replace_quotations)

os.system('clear')

print('Enter URL to novel')
novel = input()
full_link = novel

novel_ID = full_link[46:]

os.system('clear')

print(TYELLOW + 'Gathering volumes..' + TWHITE)

#Find the last page of the novel
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

#Get list of chapter numbers
while first_page < last_page+1:
    link = 'https://novel.naver.com/best/list.nhn?novelId=' + novel_ID + '&page=' + str(first_page)
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    chapter_numbers = soup.find('ul', {'class' : 'list_type2 v3 league_num NE=a:lst'})
    for a in chapter_numbers.findAll('a'):
        volume_number.append(a.get('href'))
    first_page = first_page + 1

title_of_novel = soup.find('h2', {'class' : 'book_title'}).get_text()

#Store chapter numbers in list.
for link in volume_number:
    vol_num = link[41:]
    chapter_number.append(vol_num)
chapter_number.reverse()

volumes = len(chapter_number)

os.system('clear')

print('Extracting ' + TYELLOW + str(volumes) + TWHITE + ' volumes')
print('Novel: ' + TPURPLE + title_of_novel + TWHITE)

#Scrape each chapter and save it as .txt file.
for num in tqdm(chapter_number):
    pagenumber = pagenumber + 1
    novel_link = 'https://novel.naver.com/best/detail.nhn?novelId=' + novel_ID + '&volumeNo=' + num
    response2 = requests.get(novel_link)
    soup2 = BeautifulSoup(response2.text, 'html.parser')
    title = soup2.find('a', {'class' : 'tit_book N=a:flt.end'}).get_text()
    one_p_tag = soup2.findAll('p')[0].next
    with open(title + str(pagenumber) + '.txt', 'w') as text_file:
        chuu = re.sub(' +', ' ',one_p_tag)
        print(chuu.translate(table2), file=text_file)

print('\n')
print(TWHITE + 'Finished scraping ' + TPURPLE + title + TWHITE)

