#!python34

import os.path, requests, html5lib
from bs4 import BeautifulSoup as bs


#first_link = "/sysmonitor"
#second_link = "/rps/jstatpri.cgi"
#third_link = "/rps/dcounter.cgi"


def separator(city):
    with open('C:\\Users\\00015\\Desktop\\meter_readings.txt', 'a') as file:
        if len(city) % 2 == 0:
            stars = int((18 - len(city))/2)
            file.write('\n\n' + '*' * 18 + '\n' + '*' * stars + city + '*' * stars + '\n' + '*' * 18 + '\n')
        else:
            stars = int((17 - len(city))/2)
            file.write('\n\n' + '*' * 17 + '\n' + '*' * stars + city + '*' * stars + '\n' + '*' * 17 + '\n')
    file.close()


def canon(url, copier, specific_meters):
    s=requests.Session()
    meter = []
    meters = []
    pins = ['DAL-MFP-K', 'NYC-MFP-B', 'DAL-MFP-H']
    no_argos = ['DAL-MFP-J', 'DAL-MFP-M', 'LAX-JOBSI']

    if copier[:9] in pins:
        params={'pin': '00015', 'originally-requested-url': '/rps/'}
        s.get(url + '/login', params=params)
        s.get(url + '/sysmonitor', params=params)  # have to go through all of these url for it to work
        s.get(url + '/rps/jstatpri.cgi', params=params)
        counters = s.get(url + '/rps/dcounter.cgi', params=params)
        soup = bs(counters.content, 'html5lib')
        table = soup.table
        script = table.find_all('script')    
    elif copier[:9] in no_argos:
        params={'deptid': '8888', 'loginType': 'admin', 'password': '', 'uri': '/', 'user_type_generic': ''}
        s.get(url, params=params)
        s.get(url + '/sysmonitor', params=params)  # have to go through all of these url for it to work
        s.get(url + '/rps/jstatpri.cgi', params=params)
        counters = s.get(url + '/rps/dcounter.cgi', params=params)
        soup = bs(counters.content, 'html5lib')
        table = soup.table
        script = table.find_all('script')
    elif 'PHX-MFP-B' in copier:
        params = {'password': '00015', 'uri': '/rps/'}
        s.get(url, params=params)
        s.get(url + '/rps/dstatus.cgi', params=params)  # have to go through all of these url for it to work
        counters = s.get(url + '/rps/dcounter.cgi', params=params)
        soup = bs(counters.content, 'html5lib')
        table = soup.findAll('table')
        table=table[2]
        script = table.find_all('script')
    else:
        params={'password': '00015', 'uri': '/rps/'}
        s.get(url, params=params)
        s.get(url + '/sysmonitor', params=params)  # have to go through all of these url for it to work
        s.get(url + '/rps/jstatpri.cgi', params=params)
        counters = s.get(url + '/rps/dcounter.cgi', params=params)
        soup = bs(counters.content, 'html5lib')
        table = soup.table
        script = table.find_all('script')

    for tag in script:  # Everything here and below is just parsing out the data from html/java
      tag = tag.text
      if 'write_value' in tag:
        meter.append(tag)    
    count=0
    for i in meter:
        a=i.index('(')
        b=i.index(')')
        i=i[a:b+1]
        meter[count]=i
        count=count+1
    for i in meter:
      if i[2:5] in '105109124125108':
        i=i.replace('"', '')
        meters.append(i)
    count=0
    for i in range(len(meters)):
      a=[meters[count][1:4], meters[count][5:-1]]
      meters[count]=a
      count=count+1
    with open('C:\\Users\\00015\\Desktop\\meter_readings.txt', 'a') as f:
      f.write('\n' + copier + '\n')
      for i in meters:
        if i[0] in specific_meters:
          f.write(i[0] + ': ' + i[1] + '\n')

def xerox(url, copier):
    r = requests.get(url)  # get info and make soup
    soup = bs(r.text, 'html5lib')
    script = soup.find_all('script')      # parse the meter readings from java
    my_script = script[0].text
    binfo = my_script.split('var billInfo = ')
    binfo2 = str(binfo[1]).rsplit(';')      # parse the meter readings from java
    result = binfo2[0].replace('[', '').replace(']', '').replace(';', '').replace('\'', '').strip().split(',')
    if 'MFP-T' in copier:
        a = result[:2]
        b = result[2:4]
        c = result[6:8]
        d = result[8:]
    else:
        a = result[:2]
        b = result[3:5]
        c = result[9:11]
        d = result[12:14]
    results = [a, b, c, d]
    with open('C:\\Users\\00015\\Desktop\\meter_readings.txt', 'a') as file:
        file.write('\n' + copier + '\n')
        for item in results:
            file.write(str(item[0]) + ': ' + str(item[1]) + '\n')