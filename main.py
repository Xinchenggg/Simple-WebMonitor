import requests
import bs4
import re
import time
import flask

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
    for url, key in zip(urls, keys):
        print(url)
        try:
            respond = requests.get(url, timeout= 5)
        except (requests.exceptions.RequestException, ValueError) as e:
            print('Error!', end=' ') 
            print(e)
            continue
        print(time_stamp, end=' ')
        if respond.status_code != 200:
            print('DOWN', end=' ')
        else:
            print('UP  ', end=' ')
        respond_time = respond.elapsed.total_seconds()
        print(respond_time, end=' ')
        html = requests.get(url).text 
        key_count = len(re.findall(key, html))
        print(f"Search for '{key}' ", end=' ')
        if key_count > 0 :
            print(f"{key_count} found")
        else:
            print('No results')

if __name__ == '__main__':
    while True:
        web_monitor()
        print()
        time.sleep(5)