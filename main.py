#!python3

import requests
from bs4 import BeautifulSoup as bs
from printers import printer_dict
import time
import re


def parse_it(s, url, params): # navigates to and collects the meter data
    meters = []
    s.get(url + '/login', params=params)
    s.get(url + '/sysmonitor', params=params)
    s.get(url + '/rps/jstatpri.cgi', params=params)
    counters = s.get(url + '/rps/dcounter.cgi', params=params)
    soup = bs(counters.content, 'html5lib')  # parsing from full page to just the meters
    reads = re.findall('write_value\((\"[0-9]+\",[0-9]+)', str(soup))
    for i in reads:
        i=i.replace('"', '').split(',')
        if i[0] in '109124105125108':
            meters.append(i)
    return meters

def canon(copier):
    s=requests.Session()
    url = copier['url']
    params = copier['params']
    specific_meters = copier['specific_meters']
    label = copier['label']


    if copier == printer_dict['PHX-MFP-B']:
        meters = []
        s.get(url, params=params)
        s.get(url + '/rps/dstatus.cgi', params=params)  # have to go through all of these url for it to work
        counters = s.get(url + '/rps/dcounter.cgi', params=params)
        soup = bs(counters.content, 'html5lib')
        reads = re.findall('write_value\((\"[0-9]+\",[0-9]+)', str(soup))
        for i in reads:
            i=i.replace('"', '').split(',')
            if i[0] in '109124105125108':
                meters.append(i)

    else:
         meters = parse_it(s, url, params)


    with open('C:\\Users\\00015\\Desktop\\meter_readings.txt', 'a') as f:  # writing meters to file
        f.write('\n' + label + '\n')
        for i in meters:
            if i[0] in specific_meters:
                f.write(i[0] + ': ' + i[1] + '\n')
        f.close()

def xerox(copier):
    global soup, meter_s, results
    url = copier['url']
    label = copier['label']
    r = requests.get(url)  # get info and make soup
    soup = bs(r.text, 'html5lib')
    meter_s = re.findall('billInfo = \[(.+)\]', str(soup))
    meter_s = meter_s[0].split(',')
    results = []
    while len(meter_s) > 0:
        temp = []
        if copier == printer_dict['DAL-MFP-E']:
            meter_s.pop()
        temp.append(meter_s.pop().replace('\'', ''))
        temp.append(meter_s.pop().replace('\'', ''))
        results.append(temp[::-1])

    with open('C:\\Users\\00015\\Desktop\\meter_readings.txt', 'a') as file:  # writing data to file
        file.write('\n' + label + '\n')
        for item in results:
            if 'Total Impressions' not in item[0]:
                file.write(item[0] + ': ' + item[1] + '\n')
        file.close()


if __name__ == '__main__':
    start = time.time()
    for item in printer_dict:
        if printer_dict[item]['brand'] == 'canon':
            try:
                canon(printer_dict[item])
            except:
                with open('C:\\Users\\00015\\Desktop\\meter_readings.txt', 'a') as f:  # writing meters to file
                    f.write('\n' + printer_dict[item]['label'] + '\n')
                    f.write('ERROR: NO METERS TAKEN\n')
                    f.close()
        elif printer_dict[item]['brand'] == 'xerox':
            xerox(printer_dict[item])
        print('Finished with {}'.format(item))
    end = time.time() - start

    print('Completed in {} minutes and {} seconds'.format(int(end//60), int(end%60)))
