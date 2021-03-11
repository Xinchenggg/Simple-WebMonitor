import requests
import re
import time

def web_monitor():
    global urls
    global keys
    urls = []
    keys = []
    time_stamp = time.ctime()
    
    with open('weblist.txt', 'r') as weblist:
        for line in weblist:
            fields = line.split(', ')
            urls.append(fields[0].strip())
            keys.append(fields[1].strip())
    with open('web.log', 'w') as log:
        log.write('###  Webpage monitor log:')
    log = open('web.log', 'a')
    for url, key in zip(urls, keys):
        log.write('\n' + url + '\n')
        try:
            respond = requests.get(url, timeout= 5)
        except (requests.exceptions.RequestException, ValueError) as e:
            log.write('Error!' + str(e))
            continue
        if respond.status_code != 200:
            log.write(time_stamp + ' DOWN ')
        else:
            log.write(time_stamp + ' UP   ')
        respond_time = round(respond.elapsed.total_seconds() * 1000, 2)
        log.write(str(respond_time)+ 'ms ')
        html = requests.get(url).text 
        key_count = len(re.findall(key, html))
        log.write(f"Search for '{key}' ")
        if key_count > 0 :
            log.write(f"{key_count} found")
        else:
            log.write('No results')
    log.close()

if __name__ == '__main__':
    while True:
        web_monitor()
        print()
        time.sleep(5)