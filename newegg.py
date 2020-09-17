'''
Webscraper created by Phillip Kluge. This webscraper uses BeautifulSoup4 as a dependency, make sure you have that and Python3 installed.
Make sure that you do not use this too often as Newegg will detect it as a DOS attack or a script; dont go overboard ;)

Version: 1.0.1

Github: @phillipkluge
LinkedIn: @phillipjkluge
Twitter: @phillipjkluge

'''

# importing all necessary dependencies
from urllib.request import urlopen as urlreq
from bs4 import BeautifulSoup as bsoup
import csv

def scraper(target_url):

	if (target_url == 'https://www.newegg.ca/p/pl?N=100007670%2050001157&cm_sp=Cat_CPU-Processors_8-_-Visnav-_-Intel-CPU&page=1'):
		titles = "brand, product_name, sale_percentage, price, shipping, total, url_link \n"
		file_name = "newegg.csv"
		f = open(file_name, "w")
		f.write(titles)
	else:
		file_name = "newegg.csv"
		f = open(file_name, "a")

	# setting the target URL, downloading the page, reading the contents, and dumping it into a variable called url_page_dump
	url_page_download = urlreq(target_url)
	url_page_dump = url_page_download.read()
	url_page_download.close()

	# parses the dumped page into html
	page_soup = bsoup(url_page_dump, "html.parser")

	# finds the total number of pages
	num_of_pages = (page_soup.find_all("span", {"class":"list-tool-pagination-text"}))[0].strong.text[2:]
	#print(num_of_pages)

	# looping through all the found pages
	for i in range(1, int(num_of_pages) + 1):
		target_url = target_url[0:-1] + str(i)
		#print(target_url)

		url_page_download = urlreq(target_url)
		url_page_dump = url_page_download.read()
		page_soup = bsoup(url_page_dump, "html.parser")

		# finds every product listing on the current page
		item_containers = page_soup.find_all("div", {"class":"item-container"})
		#print(len(item_containers))

		#loops through all the products (container) and returns useful information about them
		for container in item_containers:
		
			# finds the product brand
			try:
				product_brand = container.find("a", {"class":"item-brand"}).img["title"]
			except:
				product_brand = 'Unknown Brand'
			print(product_brand)

			# finds the product name
			try:
				product_name = container.find("a", {"class":"item-title"}).text
			except:
				product_name = "Unknown Name"
			print(product_name)


			# finds the sale percentage
			try:
				product_sale_percent = container.find("span", {"class":"price-save-percent"}).text
			except:
				product_sale_percent = "0%"
			print(product_sale_percent)

			# finds the product price and replaces a comma with nothing if there exists one in the price
			try:
				product_price_dollars = container.find("li", {"class":"price-current"}).strong.text
				product_price_cents = container.find("li", {"class":"price-current"}).sup.text
				product_price = (product_price_dollars + product_price_cents)
			except:
				product_price = "0"
			if ("," in product_price):
				product_price = product_price.replace(",", "")
			print(product_price)

			# finds the product shipping price
			product_shipping_price = container.find("li", {"class":"price-ship"}).text
			if (product_shipping_price[0] == "$"):
				product_shipping_price = product_shipping_price[1:product_shipping_price.find(" ")]
			elif (product_shipping_price == "Free Shipping"):
				product_shipping_price = "0"
			else:
				product_shipping_price = "0"
			print(product_shipping_price)

			# calculates the total product price with shipping included (also limits the float value to 2 decimal places)
			try:
				total_product_price = '%.2f' % (float(product_price) + float(product_shipping_price))
				if (total_product_price == "0"):
					total_product_price = 'Unknown Price'
			except:
				total_product_price = product_price
			print(total_product_price)

			try:
		 		product_link = container.find("a", {"class":"item-title"})["href"]
			except:
		 		product_link = 'https://newegg.ca'
			print(product_link)

			f.write(product_brand + "," + product_name.replace(",", ";") + "," + product_sale_percent + "," + product_price + "," + product_shipping_price + "," \
				+ total_product_price + "," + product_link + "\n")
	print('debug_1')
	f.close()