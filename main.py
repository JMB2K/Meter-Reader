#!python3

import requests, time, re
from printers import printer_dict

def get_meters(copier): # navigates to and collects the meter data
    meters = []
    if copier['brand'] == 'canon':
        s=requests.Session()

        for site in copier['login_path']:
            counters = s.get(copier['url'] + site, params=copier['params'])

        reads = re.findall('write_value\((\"[0-9]+\",[0-9]+)', counters.text)
        for i in reads:
            i=i.replace('"', '').split(',')
            if i[0] in '109124105125108':
                meters.append(i)
    elif copier['brand'] == 'xerox':
        r = requests.get(copier['url'])  # get info and make soup
        data = re.findall('billInfo = \[(.+)\]', r.text)
        data = data[0].split(',')
        while len(data) > 0:
            temp = []
            if copier == printer_dict['DAL-MFP-E']:
                data.pop()
            temp.append(data.pop().replace('\'', ''))
            temp.append(data.pop().replace('\'', ''))
            meters.append(temp[::-1])
    return meters

def write_to_file(copier, meters):
    with open('C:\\Users\\00015\\Desktop\\meter_readings.txt', 'a') as f:  # writing meters to file
        f.write('\n{}\n'.format(copier['label']))
        if copier['brand'] == 'canon':
            for item in meters:
                if item[0] in copier['specific_meters']:
                    f.write('{}: {}\n'.format(item[0], item[1]))
        elif copier['brand'] == 'xerox':
            for item in meters:
                if 'Total Impressions' not in item[0]:
                    f.write('{}: {}\n'.format(item[0], item[1]))
        f.close()


if __name__ == '__main__':
    start = time.time()
    for item in printer_dict:
        try:
            meters = get_meters(printer_dict[item])
            write_to_file(printer_dict[item], meters)
        except Exception:
            with open('C:\\Users\\00015\\Desktop\\meter_readings.txt', 'a') as f:  # writing meters to file
                f.write('\n' + printer_dict[item]['label'] + '\n')
                f.write('ERROR: NO METERS TAKEN\n')
                f.close()

        print('Finished with {}'.format(item))
    end = time.time() - start

    print('Completed in {} minutes and {} seconds'.format(int(end//60), int(end%60)))
