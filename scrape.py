import requests,re,os
from collections import deque
import urllib.parse
from bs4 import BeautifulSoup
os.system('clear')
ee = '\x1b[33;5m'
logo = f'''{ee}
 ___  ___ _ __ __ _ _ __   ___ _ __
/ __|/ __| '__/ _` | '_ \ / _ \ '__|
\__ \ (__| | | (_| | |_) |  __/ |
|___/\___|_|  \__,_| .__/ \___|_| \n'''
print(logo)
url_target = str(input('[:] Masukan Url : '))
urls = deque([url_target])
scrape_url = set()
email1 = set()
count = 0
limit = int(input('[:] Masukan Limit : '))
ditemukan = 0
bb ='\x1b[32;5m'
cc ='\x1b[36;5m'

try:
	while True:
		count+=1
		if count > limit:
			break
		url = urls.popleft()
		scrape_url.add(url)
		srapesplit = urllib.parse.urlsplit(url)
		base_url = f'{srapesplit.scheme}://{srapesplit.netloc}'
		path = url[:url.rfind('/')+1] if '/' in srapesplit.path else url
		print(f'{bb}[{count}] : {url}')
		try:
			response = requests.get(url)
		except(requests.exceptions.MissingSchema, requests.excetions.ConnectionError):
			continue
		new_email = set(re.findall(r'[a-z0-9\.\-+_]+@\w+\.+[a-z\.]+',response.text, re.I))
		email1.update(new_email)
		soup = BeautifulSoup(response.text,'html.parser')
		for achor in soup.find_all('a'):
			link = achor.attrs['href'] if 'href' in achor.attrs else ''
			if link.startswith('/'):
				link = base_url + link
			elif not link.startswith('http'):
				link = path + link
			if not link in urls and not link in email1:
				urls.append(link)

except KeyboardInterrupt:
	print('[:] Closing')

print(f'{cc}{len(email1)} email di termukan')

for mail in email1:
	ditemukan+=1
	print(f'{cc}[{ditemukan}] : {mail}')
print('\n')
