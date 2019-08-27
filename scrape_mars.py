import pandas as pd
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist

def init_browser():
	executable_path = {'executable_path': 'chromedriver.exe'}
	return Browser('chrome', **executable_path, headless=False)

def scrape():
	browser = init_browser()
	data = {}
	url = 'https://mars.nasa.gov/news/'
	browser.visit(url)
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')
	list_news = soup.find('ul', class_='item_list')
	last_news = list_news.find_all('li')[0]
	link_news = last_news.find('a')['href']
	url = 'https://mars.nasa.gov' + link_news
	browser.visit(url)
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')
	title = soup.find('h1', class_='article_title')
	title = title.text
	title = title[1:]
	title = title[:-1]
	par_list = soup.find('div', class_='wysiwyg_content')
	par = par_list.find_all('p')[0]
	para = par.text
	url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	browser.visit(url)
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')
	carousel_item = soup.find('article', class_="carousel_item")
	footer = carousel_item.find('footer')
	fig_id = footer.find('a')['data-link']
	fig_id = fig_id.split("=")[1]
	featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/' + fig_id + '_ip.jpg'
	data["featured_image_url"]
	url = "https://twitter.com/marswxreport?lang=en"
	browser.visit(url)
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')
	stream = soup.find('ol', class_='stream-items js-navigable-stream')
	stream2 = stream.find_all('li')[0]
	stream3 = stream2.find('div', class_='js-tweet-text-container')
	mars_weather = stream3.find('p').text
	data["mars_weather"] = mars_weather
	url = "https://space-facts.com/mars/"
	tables = pd.read_html(url)
	df = tables[1]
	df.rename(columns={0:'Info',1:'Value'}, inplace=True)
	df.set_index('info', inplace=True)
	html_table = df.to_html()
	html_table = html_table.replace('\n', "")
	data["html_table"] = html_table
	url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	browser.visit(url)
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')
	urls =[]
	list = soup.find('div', class_='collapsible results')
	lists = list.find_all('div', class_="item")

	for item in lists:
	    desc = item.find('div', class_='description')
	    urls.append('https://astrogeology.usgs.gov' +  desc.find('a')['href'])

	hemi = []
	for url in urls:
	    browser.visit(url)
	    html = browser.html
	    soup = BeautifulSoup(html, 'html.parser')
	    html = soup.find('div', class_='downloads')
	    img = 'https://astrogeology.usgs.gov' + html.find('img')['src']
	    title = soup.title.text
	    title = title.split("|")[0]
	    title = title.replace("Enhanced","")
	    hemi.append({"title":title, "img": img})
	data["hemi"] = hemi
	return data