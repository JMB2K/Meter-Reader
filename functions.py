#!python34

import requests, html5lib, timing
from bs4 import BeautifulSoup as bs


def separator(city):
    with open('C:\\Users\\00015\\Desktop\\meter_readings.txt', 'a') as file:
        if len(city) % 2 == 0:
            stars = int((18 - len(city))/2)
            file.write('\n\n' + '*' * 18 + '\n' + '*' * stars + city + '*' * stars + '\n' + '*' * 18 + '\n')
        else:
            stars = int((17 - len(city))/2)
            file.write('\n\n' + '*' * 17 + '\n' + '*' * stars + city + '*' * stars + '\n' + '*' * 17 + '\n')
    file.close()

def parse_it(s, url, params): # navigates to and collects the meter data
    s.get(url + '/login', params=params)
    s.get(url + '/sysmonitor', params=params)
    s.get(url + '/rps/jstatpri.cgi', params=params)
    counters = s.get(url + '/rps/dcounter.cgi', params=params)
    soup = bs(counters.content, 'html5lib')  # parsing from full page to just the meters
    table = soup.table
    script = table.find_all('script')
    return script

def canon(url, copier, specific_meters):
    s=requests.Session()
    meters = []
    pins = ['DAL-MFP-K', 'NYC-MFP-B', 'DAL-MFP-H'] # argos onboard installed but uses pin instead of password in html
    no_argos = ['DAL-MFP-J', 'DAL-MFP-M', 'LAX-JOBSI']  # no argos installed, uses the canon UI

    if 'PHX-MFP-B' in copier:
        params = {'password': '00015', 'uri': '/rps/'}
        s.get(url, params=params)
        s.get(url + '/rps/dstatus.cgi', params=params)  # have to go through all of these url for it to work
        counters = s.get(url + '/rps/dcounter.cgi', params=params)
        soup = bs(counters.content, 'html5lib')
        table = soup.findAll('table')
        table=table[2]
        script = table.find_all('script')

    else:
        if copier[:9] in pins:
            params={'pin': '00015', 'originally-requested-url': '/rps/'}
        elif copier[:9] in no_argos:
            params={'deptid': '8888', 'loginType': 'admin', 'password': '', 'uri': '/', 'user_type_generic': ''}
        else:
            params={'password': '00015', 'uri': '/rps/'}
        script = parse_it(s, url, params)

    for item in script:  #  getting rid of all the bs and down to meter data only
        item=item.text
        if 'write_value' in item:
            a=item.index('(')
            b=item.index(')') + 1
            item = item[a:b].replace('"', '')
            if item[1:4] in '109105124125108':
                a=item[1:4]
                b=item[5:-1]
                meters.append([a, b])

    with open('C:\\Users\\00015\\Desktop\\meter_readings.txt', 'a') as f:  # writing meters to file
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
    if 'MFP-T' in copier:  # organizing the data so it writes to file how I want it to
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
    with open('C:\\Users\\00015\\Desktop\\meter_readings.txt', 'a') as file:  # writing data to file
        file.write('\n' + copier + '\n')
        for item in results:
            file.write(str(item[0]) + ': ' + str(item[1]) + '\n')
