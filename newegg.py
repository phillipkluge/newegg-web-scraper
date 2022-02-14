'''
Webscraper created by Phillip Kluge.
This webscraper uses BeautifulSoup4 as a dependency,
make sure you have that and Python3 installed.

Make sure that you do not use this too often as Newegg will detect
it as a DOS attack or a script; a VPN is recommended!

Version: 3.0.0 B1
Current Release: 2022/02/11
Original Release: 2021/01/10

Github: @phillipkluge
LinkedIn: @phillipjkluge

This file conforms to the PEP-8 style guide.
'''

# importing all necessary dependencies
from urllib.request import urlopen as urlreq
from xmlrpc.client import Boolean, boolean
from bs4 import BeautifulSoup as bsoup
import datetime
from time import sleep
from handler import Errors, Inputs, Handler
from constants import *

class Scraper:

    intel = None  # allocates the intel link from the driver
    amd = None  # allocates the amd link from the driver

    _delay = None  # the delay between pages
    _first = True  # boolean True if it's the program's first run through
    _repeat = None  # boolean True if the program needs to repeat for another URL
    _page_limit = None  # the number of pages to scrape through
    _target_url = None  # the current selected URL to scrape
    _done = False

    def __init__(self, intel, amd) -> None:
        # sets the inital variables
        self.intel = intel
        self.amd = amd
        self._delay = 0

        # setting up the desired behavior behavior
        cpu_setting = input("Enter a custom link for scraping? (y/n): ")
        cpu_setting = cpu_setting.lower()
        cpu_setting = Handler.input_handler(type=Inputs.YES_NO,stat_input=cpu_setting)
        if cpu_setting == "y":
            print("Enter a custom URL that you wish to scrape")
            print("***Make sure that the url has '&page=1' at the end!!!")
            num_setting = input("Input: ")
            num_setting = Handler.input_handler(type=Inputs.URL,stat_input=num_setting)

        else:
            num_setting = input("Press 1 for the Intel URL, "
                                "2 for the AMD, or 3 for both: ")
            num_setting = Handler.input_handler(type=Inputs.NUMBER,stat_input=num_setting,lower=1,upper=3)

        page_setting = input("Limit the number of pages scraped? (y/n): ")
        page_setting = page_setting.lower()
        page_setting = Handler.input_handler(type=Inputs.YES_NO,stat_input=page_setting)
        if page_setting == "y":
            self._page_limit = input("Max number of pages: ")
            self._page_limit = Handler.input_handler(type=Inputs.NUMBER,stat_input=self._page_limit,lower=1)
        else:
            self._page_limit = -1

        if (self._page_limit != 1):
            ask_delay = input("Add a delay between each page? "
                            "May reduce proliferation of errors. (y/n): ")
            ask_delay = ask_delay.lower()
            ask_delay = Handler.input_handler(type=Inputs.YES_NO,stat_input=ask_delay)
            if ask_delay == "y":
                delay_in = input("Delay (in seconds) (1-9) : ")
                delay_in = Handler.input_handler(type=Inputs.NUMBER,stat_input=delay_in,lower=1,upper=9)
                self._delay = delay_in
            else:
                print("No delay specified... continuing program execution")

        try:
            num_setting = int(num_setting)
            if num_setting == 1:
                self._target_url = self.intel
                self._repeat = False

            elif num_setting == 2:
                self._target_url = self.amd
                self._repeat = False

            elif num_setting == 3:
                self._target_url = self.intel
                self._repeat = True
        except:
            Handler.error_handler(type=Errors.URL_SET,exit=True,delay=3)

    def __del__(self):
        print("\n" + Formatting.PROGRAM_HEADER)
        Handler.clean(self._done)
        print(Formatting.PROGRAM_HEADER)
        

    def scrape(self) -> None:
        if self._first:
            titles = ("brand, product_name, sale_percentage, price, "
                      "shipping, total, url_link")
            file_name = "newegg.csv"
            try:
                f = open(file_name, "w")
            except PermissionError:
                Handler.error_handler(type=Errors.FILE,exit=True,delay=3)
            currentDate = str(datetime.datetime.now())
            f.write(titles + ",,," + currentDate + "\n")
            print("\nCollecting data, be patient!...")
        else:
            file_name = "newegg.csv"
            try:
                f = open(file_name, "a")
            except PermissionError:
                Handler.error_handler(type=Errors.FILE,exit=True,delay=3)

        # setting the target URL, downloading the page, reading the contents,
        # and dumping it into a variable called url_page_dump
        url_page_download = urlreq(self._target_url)
        url_page_dump = url_page_download.read()
        url_page_download.close()

        # parses the dumped page into html
        page_soup = bsoup(url_page_dump, "html.parser")

        # finds the total number of pages
        try:
            num_of_pages = (page_soup.find_all(
                "span",
                {"class": "list-tool-pagination-text"}))[0].strong.text[2:]
        except:
            num_of_pages = "1"

        # looping through all the found pages
        for i in range(1, int(num_of_pages) + 1):
            if ((i > self._page_limit) and (self._page_limit != -1)):
                break

            if i == self._page_limit:
                page_limit_test = True
            else:
                page_limit_test = False

            digit_length = len(str(i - 1))
            self._target_url = self._target_url[0:-digit_length] + str(i)

            url_page_download = urlreq(self._target_url)
            url_page_dump = url_page_download.read()
            page_soup = bsoup(url_page_dump, "html.parser")

            try:
                anchor_element = page_soup.find(
                    "div", {"class": "list-tool-search"}).label.text
                if anchor_element != "Search Within:":
                    Handler.error_handler(type=Errors.BOT, exit=True, delay=3)
            except AttributeError:
                Handler.error_handler(type=Errors.BOT, exit=True, delay=3)

            # finds every product listing on the current page
            item_containers = page_soup.find_all(
                "div", {"class": "item-container"})

            # loops through all the products (container) and
            # returns useful information about them
            for container in item_containers:

                # finds the product brand
                try:
                    product_brand = container.find(
                        "a", {"class": "item-brand"}).img["title"]
                except:
                    product_brand = "Unknown Brand"

                # finds the product name
                try:
                    product_name = container.find(
                        "a", {"class": "item-title"}).text
                except:
                    product_name = "Unknown Name"

                # finds the sale percentage
                try:
                    product_sale_percent = container.find(
                        "span", {"class": "price-save-percent"}).text
                    if product_sale_percent[-1] != "%":
                        product_sale_percent = "0%"
                except:
                    product_sale_percent = "0%"

                # finds the product price and replaces a comma with
                # nothing if there exists one in the price
                try:
                    product_price_dollars = container.find(
                        "li", {"class": "price-current"}).strong.text
                    product_price_cents = container.find(
                        "li", {"class": "price-current"}).sup.text
                    product_price = \
                        (product_price_dollars + product_price_cents)
                except:
                    product_price = "0"
                if ("," in product_price):
                    product_price = product_price.replace(",", "")

                # finds the product shipping price
                try:
                    product_shipping_price = container.find(
                        "li", {"class": "price-ship"}).text
                except:
                    product_shipping_price = "0"
                if (product_shipping_price == ""):
                    product_shipping_price = "0"
                elif (product_shipping_price[0] == "$"):
                    product_shipping_price = product_shipping_price[
                        1:
                        product_shipping_price.find(" ")]
                elif (product_shipping_price == "Free Shipping"):
                    product_shipping_price = "0"
                else:
                    product_shipping_price = "0"

                # calculates the total product price with shipping included
                # (also limits the float value to 2 decimal places)
                try:
                    total_product_price = "%.2f" % \
                        (float(product_price) + float(product_shipping_price))
                    if (total_product_price == "0"):
                        total_product_price = "Unknown Price"
                except:
                    total_product_price = product_price

                try:
                    product_link = container.find(
                        "a", {"class": "item-title"})["href"]
                except:
                    product_link = "https://newegg.ca"

                f.write(product_brand + "," + product_name.replace(
                    ",", ";") + "," + product_sale_percent + "," +
                    product_price + "," + product_shipping_price + "," +
                    total_product_price + "," + product_link + "\n")

            if ((self._delay != 0) and (i != int(num_of_pages)) and
                    (not page_limit_test)):

                for i in range(0, self._delay + 1):
                    print("Delay time left: " + str(
                          self._delay - i), end="\r")
                    sleep(1)

        f.close()

        if self._repeat:
            self._repeat = False
            self._first = False

            self._target_url = self.amd

            self.scrape()
        else:
            self._done = True
