import requests
import bs4
import re
import time, threading

def main():
    global urls
    global keys
    urls = []
    keys = []
    count = 0

    with open('weblist.txt', 'r') as weblist:
        for line in weblist:
            fields = line.split(', ')
            urls.append(fields[0].strip())
            keys.append(fields[1].strip())
    list_size = len(urls)
    # print(urls)            
    # print(keys)

    for url in urls:
        print(url)
        respond = requests.get(url, timeout = 10)
        print(time.ctime(), end=' ')
        if respond.status_code != 200:
            print('DOWN', end=' ')
        else:
            print('UP  ', end=' ')
        print(respond.elapsed.total_seconds(), end=' ')
        
        #
        for key in keys:
            #keys = 'computer'          # should read from weblist.txt
            html = requests.get(urls[0]).text 
            for match in re.findall(key, html):
                count += 1
            with open('web.log','w') as web_log:
                print(f"Search for '{match}' ", end=' ')
                if count > 0 :
                    web_log.write(f"{count} found")
                    print(f"{count} found")
                else:
                    web_log.write('No results')
                    print('No results')

    # while True:
    #     webpage_stats()
    #     time_wait = 5
    #     print(f'Waiting {time_wait} seconds', end = '')
    #     for i in range(time_wait):
    #         print('.',end = '',flush = True)
    #         time.sleep(1)
    #     print('\n')

    
# def webpage_stats():
#     for url in urls:
#         respond = requests.get(url, timeout = 10)
#         print(respond.status_code)
#         # content = urlopen(url).read()
#         # soup = bs4.BeautifulSoup(content, 'lxml')
#         # print(soup.prettify())
#     print(time.ctime())
#     # threading.Timer(5000, webpage_stats()).start()

# def search_key():
#     regex = 'computer'          # should read from weblist.txt
#     count = 0
#     html = requests.get(urls[0]).text 
#     for match in re.findall(regex, html):
#         count += 1
#     with open('web.log','w') as web_log:
#         if count > 0 :
#             web_log.write(f"'{match}' {count} found")
#             print(f"'{match}' {count} found")
#         else:
#             web_log.write('No results')
#             print('No results')


#if respond.status_code != 200:
    #write to log

# with open('log.txt', 'w') as log:
#     log.write('test')

'''
periodlly
for loop
check web stats
if up, write in up
if down, write in down
compare web content and keywords
'''

if __name__ == '__main__':
    main()