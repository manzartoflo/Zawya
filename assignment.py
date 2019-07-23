#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 10:45:54 2019

@author: manzar
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://www.zawya.com/mena/en/companies/list/cso/?keyword=&country=&sector=&ownership=&resultsPerPage=10&page="

header = "Company name, Telephone, Fax, Email, Website\n"
file = open("assignment.csv", 'a')
file.write(header)
for i in range(1, 4551):
    req = requests.get(url + str(i))
    soup = BeautifulSoup(req.text, 'lxml')
    h3 = soup.findAll('h3')
    h3 = h3[13:23]
    for j in range(10):
        try:
            req_inside = requests.get(urljoin(url, h3[j].a.attrs['href']))
            soup_inside = BeautifulSoup(req_inside.text, 'lxml')
            title = soup_inside.findAll('h1', {'class': 'page-title'})
            try:
                name = title[0].text
            except:
                name = 'NaN'
            info = soup_inside.findAll('div', {'class': 'info-box'})
            try:
                ul = info[1].findAll('ul')
            except:
                try:
                    ul = info[0].findAll('ul')
                except:
                    pass
    
            try:
                number = ul[0].findAll('strong', {'class': 'text-number'})
            except:
                number = 'NaN'
            
            try:
                web = ul[0].findAll('a', {'target': '_blank'})
                web = web[0].attrs['href']
            except:
                web = 'NaN'
                
            try:
                email = ul[0].findAll('a', {'class': 'email'})
                email = email[0].attrs['href'].split('mailto:')[1]
            except:
                email = 'NaN'
            
            if(number != 'NaN'):
                if(len(number) == 1):
                    tel = number[0].text
                    fax = 'NaN'
                if(len(number) == 2):
                    tel = number[0].text
                    fax = number[1].text
            
            print(name, tel, fax, email, web)
            file.write(name.replace(',', '') + ', ' + tel + ', ' + fax + ', ' + email + ', ' + web + '\n')
        except:
            pass
file.close()