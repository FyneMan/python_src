#!/usr/bin/python2.7
#coding=utf-8

import re
import requests
from bs4 import BeautifulSoup

AList = {'Director':'2606', 'MaleBest':'2602', 'FemaleBest':'2603', 'MaleSupp':'2604', 'FemaleSupp':'2605', 'NewBest':'2619'}

for key in AList:
    Year = 2015
    filename = open(key+'.dat', 'w')
    url = 'http://award.mtime.com/17/award/' + AList[key] + '/'
    webdata = requests.get(url)
    soup = BeautifulSoup(webdata.content, 'html.parser')
    pages = soup.find_all("div", {"class":"pagenav tc mt20"})[0].find_all("a")
    pages_url = list()
    for item in pages:
        pages_url.append( item.get("href") )

    for jj in range(1, len(pages_url) - 1 ):
        url = pages_url[jj]
        webdata = requests.get(url)
        soup = BeautifulSoup(webdata.content, 'html.parser')
        
        AwardsTable = soup.find_all("div", {"class": "event_awards event_list"})
        Awardees = AwardsTable[0].find_all("div", {"class": "yellowbox"})
        Nominees = AwardsTable[0].find_all("div", {"class": "bluebox"})
        
        pattern1 = re.compile(r'^(\S+) \S')
        pattern2 = re.compile(r'http://people.mtime.com.(\d*)')
        mm = 0
        for item in Awardees:
            elem = item.find_all("a")
            namelist = list()
            for ii in range(1, len(elem)-1):
                searchRes = pattern1.search(elem[ii].text)
                if searchRes==None:
                    name = list()
                    name.append( elem[ii].text.strip(' \t\n\r').replace(' ', '_') )
                else:
                    name = searchRes.groups()

                num = pattern2.search(elem[ii].get("href")).groups()
                namelist.append((name[0],num[0]))

            filmRes = pattern1.search(elem[len(elem)-1].text)
            if filmRes:
                film = filmRes.groups()
            else:
                film = list()
                film.append(u' ')

            for director in namelist:
                filename.write('获奖 {0:4d} {1:10s} {2:10s} {3:20s}\n'.format(Year, director[0].encode('utf-8'), director[1].encode('utf-8'), film[0].encode('utf-8')))

            Year -= 1
            mm += 1
        
        Year += mm
        for item in Nominees:
            reviewlist = item.find_all("dl", {"class": "fix"})
            for elem in reviewlist:
                info = elem.find_all("a")
                namelist = list()
                for ii in range(1,len(info)-1):
                    searchRes = pattern1.search(info[ii].text)
                    if searchRes==None:
                        name = list()
                        name.append(info[ii].text.strip(' \t\n\r').replace(' ', '_'))
                    else:
                        name = searchRes.groups()
                    num = pattern2.search(info[ii].get("href")).groups()
                    namelist.append((name[0], num[0]))

                filmRes = pattern1.search(info[len(info)-1].text)
                if filmRes:
                    film = filmRes.groups()
                else:
                    film = list()
                    film.append(u' ')

                for director in namelist:
                    filename.write('提名 {0:4d} {1:10s} {2:10s} {3:20s}\n'.format(Year, director[0].encode('utf-8'), director[1].encode('utf-8'), film[0].encode('utf-8')))

            Year -= 1

    filename.close()
