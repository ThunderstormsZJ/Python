
# -*- coding:UTF-8 -*-
from urllib import request
from urllib.error import ContentTooShortError
from bs4 import BeautifulSoup
from urllib.request import urlretrieve, build_opener, install_opener
import requests
import os
import time

def download(url, local_url):
	try:
		urlretrieve(url = url, filename = local_url)
	except ContentTooShortError:
		download(url, local_url)


if __name__ == '__main__':
	url = 'https://eternitywith.gitee.io/galleries/%E5%8D%9A%E5%AE%A2%E8%83%8C%E6%99%AF%E5%9B%BE/'
	headers = {
			"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
	}
	req = requests.get(url = url, headers = headers, verify=False)
	req.encoding = 'utf-8'
	html = req.text
	bf = BeautifulSoup(html, 'html.parser')
	imgList = bf.find_all(attrs={"data-fancybox": "images"})
	
	root_path = os.path.dirname(__file__)
	imgs_path = os.path.join(root_path, "images")
	if not os.path.exists(imgs_path):
		os.mkdir(imgs_path)

	exist_img_list = os.listdir(imgs_path)

	
	print('1.jpg' in exist_img_list)
	opener = build_opener()
	opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")]
	install_opener(opener)

	for img in imgList:
		if img.attrs is not None:
			img_url = img.attrs['href']
			filename = img_url.split('/')[-1]
			if filename not in exist_img_list:
				print('Download: %s' % img_url)
				download(img_url, os.path.join(imgs_path, filename))

	print('Download Complete')