import requests
import re
import time
import threading
from flask import Flask, render_template, request

htmllog = []
app = Flask(__name__)

@app.route('/', methods=['GET'])
def page():
    return render_template('index.html', content = htmllog) 

def web_monitor():
    while True:
        global sleep_time
        global htmllog
        urls = []
        keys = []
        htmllog.clear()
        time_stamp = time.ctime()

        with open('weblist.txt', 'r') as weblist:
            fisrtline_config = weblist.readline()
            sleep_time = re.findall(r'[0-9]+', fisrtline_config)
            for line in weblist:
                fields = line.split(', ')
                urls.append(fields[0].strip())
                keys.append(fields[1].strip())
        with open('web.log', 'w') as log:
            log.write('###  Webpage monitor log:')
        log = open('web.log', 'a')
        for url, key in zip(urls, keys):
            response_info = ' '
            log.write('\n' + url + '\n')
            try:
                respond = requests.get(url, timeout= 5)
            except (requests.exceptions.RequestException, ValueError) as e:
                log.write('Error!' + str(e))
                response_info += 'Error!' + str(e) + ' '
                htmllog.append((url, response_info))
                continue
            if respond.status_code != 200:
                log.write(time_stamp + ' DOWN ')
                response_info += time_stamp + ' DOWN'
            else:
                log.write(time_stamp + ' UP   ')
                response_info += time_stamp + ' UP    '
            respond_time = round(respond.elapsed.total_seconds() * 1000, 2)
            log.write(str(respond_time)+ 'ms ')
            response_info += str(respond_time) + 'ms '
            html = requests.get(url).text 
            key_count = len(re.findall(key, html))
            log.write(f"Search for '{key}' ")
            response_info += f'Search for "{key}"'
            if key_count > 0 :
                log.write(f"{key_count} found")
                response_info += ' ' + str(key_count) + ' found'
            else:
                log.write('No results')
                response_info += 'No results'
            htmllog.append((url, response_info))
        log.close()
        time.sleep(int(sleep_time[0]))
    
if __name__ == '__main__':
    threading.Thread(target=web_monitor).start()
    threading.Thread(target=app.run).start()
        