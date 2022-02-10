'''
Webscraper created by Phillip Kluge.
This webscraper uses BeautifulSoup4 as a dependency,
make sure you have that and Python3 installed.

Make sure that you do not use this too often as Newegg will detect
it as a DOS attack or a script; a VPN is recommended!

Version: 2.1.0 R1
Current Release: 2022/02/10
Original Release: 2021/01/10

Github: @phillipkluge
LinkedIn: @phillipjkluge

This file conforms to the PEP-8 style guide.
'''

# importing all necessary dependencies
import urllib
from urllib.request import urlopen as urlreq
from xmlrpc.client import boolean
from bs4 import BeautifulSoup as bsoup
import csv
import datetime
from time import sleep


class Scraper:

    intel = None  # allocates the intel link from the driver
    amd = None  # allocates the amd link from the driver

    _debug = None  # state of the debug mode
    _delay = None  # the delay between pages
    _first = True  # boolean True if it's the program's first run through
    _repeat = None  # boolean True if the program needs to repeat
    _page_limit = None  # the number of pages to scrape through
    _target_url = None  # the current selected URL to scrape

    def __init__(self, intel, amd, debug) -> None:
        # sets the target URL
        self.intel = intel
        self.amd = amd
        self._debug = debug
        self._delay = 0

        # setting up the desired behavior behavior
        cpu_setting = input('Enter a CUSTOM link for scraping, \
            or use DEFAULTS? (c/d): ')
        cpu_setting = cpu_setting.lower()
        cpu_setting = input_verifier(1, cpu_setting)
        if cpu_setting == 'd':
            num_setting = input('Press 1 for the Intel URL, \
                2 for the AMD, or 3 for both: ')
            num_setting = input_verifier(3, num_setting)
        elif cpu_setting == 'c':
            print('Enter a custom URL that you wish to scrape')
            print('***Make sure that the url has "&page=1" at the end!!!')
            num_setting = input('Input: ')
            num_setting = input_verifier(2, num_setting)

        print('\n')

        page_setting = input('Limit the number of pages scraped? (y/n): ')
        page_setting = page_setting.lower()
        page_setting = input_verifier(0, page_setting)
        if page_setting == 'y':
            self._page_limit = input('Max number of pages: ')
            self._page_limit = input_verifier(5, self._page_limit)
            self._page_limit = input_verifier(7, self._page_limit)
        elif page_setting == 'n':
            self._page_limit = -1

        print('\n')

        ask_delay = input('Add a delay between each page? \
            May reduce proliferation of errors. (y/n): ')
        ask_delay = ask_delay.lower()
        ask_delay = input_verifier(0, ask_delay)
        if ask_delay == 'y':
            delay_in = input('Delay (in seconds) (1-9) : ')
            delay_in = input_verifier(5, delay_in)
            delay_in = input_verifier(6, delay_in)
            self._delay = delay_in
        else:
            print('No delay specified... continuing program execution')

        print('\n')

        try:
            num_setting = int(num_setting)
            if num_setting == 1:
                self._target_url = intel
                self._repeat = False

            elif num_setting == 2:
                self._target_url = amd
                self._repeat = False

            elif num_setting == 3:
                self._target_url = intel
                self._repeat = True
        except:
            self._target_url = num_setting
            self._repeat = False

    @classmethod
    def scrape(self) -> None:
        if self._first:
            titles = "brand, product_name, sale_percentage, price, \
                shipping, total, url_link"
            file_name = "newegg.csv"
            try:
                f = open(file_name, "w")
            except PermissionError:
                print("------ERROR------ERROR------ERROR------ERROR------ \
                    ERROR------ERROR------ERROR------")
                print("FILE OPEN ERROR! Please close the .csv file before \
                    running the program.")
                print("-------------------------------------------------- \
                    ---------------------------------")
                print('\n')
                print("Exiting program...")
                sleep(3)
                quit()
            currentDate = str(datetime.datetime.now())
            f.write(titles + ',,,' + currentDate + "\n")
            print('Collecting data, be patient!...')
            print('\n')
        else:
            file_name = "newegg.csv"
            try:
                f = open(file_name, "a")
            except PermissionError:
                print("------ERROR------ERROR------ERROR------ERROR------ \
                    ERROR------ERROR------ERROR------")
                print("FILE OPEN ERROR! Please close the .csv file before \
                    running the program.")
                print("-------------------------------------------------- \
                    ---------------------------------")
                print('\n')
                print("Exiting program...")
                sleep(3)
                quit()

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
            num_of_pages = '1'

        if self._debug:
            print('------------------------------ \
                DEBUG------------------------------')
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
            if self._debug:
                print('PAGE URL: ' + str(self._target_url))

            url_page_download = urlreq(self._target_url)
            url_page_dump = url_page_download.read()
            page_soup = bsoup(url_page_dump, "html.parser")

            try:
                anchor_element = page_soup.find(
                    "div", {"class": "list-tool-search"}).label.text
                if anchor_element != "Search Within:":
                    print("\n")
                    print("------ERROR------ERROR------ERROR------ \
                        ERROR------ERROR------ERROR------ERROR------")
                    print("Newegg has likely detected this as a bot \
                        ! Please consider adding a delay, limiting")
                    print("pages, and changing the VPN server location!")
                    print("---------------------------------------- \
                        -------------------------------------------")
                    print("\n")
                    print("Exiting program...")
                    sleep(3)
                    quit()
            except AttributeError:
                print("\n")
                print("------ERROR------ERROR------ERROR------ERROR------ \
                    ERROR------ERROR------ERROR------")
                print("Newegg has likely detected this as a bot! Please \
                    consider adding a delay, limiting")
                print("pages, and changing the VPN server location!")
                print("-------------------------------------------------- \
                    ---------------------------------")
                print("\n")
                print("Exiting program...")
                sleep(3)
                quit()

            # finds every product listing on the current page
            item_containers = page_soup.find_all(
                "div", {"class": "item-container"})

            # loops through all the products (container) and
            # returns useful information about them
            for container in item_containers:
                if self._debug:
                    print('PAGE: ' + str(i))

                # finds the product brand
                try:
                    product_brand = container.find(
                        "a", {"class": "item-brand"}).img["title"]
                except:
                    product_brand = 'Unknown Brand'
                if self._debug:
                    print('BRAND: ' + product_brand)

                # finds the product name
                try:
                    product_name = container.find(
                        "a", {"class": "item-title"}).text
                except:
                    product_name = "Unknown Name"
                if self._debug:
                    print('PRODUCT NAME: ' + product_name)

                # finds the sale percentage
                try:
                    product_sale_percent = container.find(
                        "span", {"class": "price-save-percent"}).text
                    if product_sale_percent[-1] != "%":
                        product_sale_percent = "0%"
                except:
                    product_sale_percent = "0%"
                if self._debug:
                    print('SALE PERCENT: ' + product_sale_percent)

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
                if self._debug:
                    print('PRICE: ' + product_price)

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
                if self._debug:
                    print('SHIPPING PRICE: ' + product_shipping_price)

                # calculates the total product price with shipping included
                # (also limits the float value to 2 decimal places)
                try:
                    total_product_price = '%.2f' % \
                        (float(product_price) + float(product_shipping_price))
                    if (total_product_price == "0"):
                        total_product_price = 'Unknown Price'
                except:
                    total_product_price = product_price
                if self._debug:
                    print('TOTAL PRICE: ' + total_product_price)

                try:
                    product_link = container.find(
                        "a", {"class": "item-title"})["href"]
                except:
                    product_link = 'https://newegg.ca'
                if self._debug:
                    print('URL: ' + product_link)

                f.write(product_brand + "," + product_name.replace(
                    ",", ";") + "," + product_sale_percent + "," +
                    product_price + "," + product_shipping_price + "," +
                    total_product_price + "," + product_link + "\n")
                if self._debug:
                    print('_______________________ \
                        ______________________________')

            if ((self._delay != 0) and (i != int(num_of_pages)) and
                    (not page_limit_test)):
                if self._debug:
                    print('\n')
                    print('------------------------ \
                        DEBUG------------------------')
                    print('Delaying for ' + str(
                        self._delay) +
                        ' second(s)')
                    print('------------------------ \
                        -----------------------------')

                for i in range(0, self._delay):
                    if self._debug:
                        print('Delay time left: ' + str(
                            self._delay - i), end="\r")
                    sleep(1)

                if self._debug:
                    print('\n')
                    print('________________________ \
                        _____________________________')

        if self._debug:
            print('-------------------------------- \
                ---------------------------------')
            print('\n')
            print('------------------------ \
                DEBUG------------------------')
            print('End of main sequence reached!')
            print('------------------------ \
                -----------------------------')

        f.close()

        if self._repeat:
            if self._debug:
                print('\n')
                print('------------------------ \
                    DEBUG------------------------')
                print('Repeat sequence reached!')
                print('------------------------ \
                    -----------------------------')
                print('\n')
            self._repeat = False
            self._first = False

            self._target_url = self.amd

            self.scrape()


def input_verifier(ver_code, stat_input) -> str:
    trip = False

    # Verifier for the (y/n) questions
    if ver_code == 0:
        while ((stat_input != 'y') and (stat_input != 'n')):
            trip = True
            stat_input = input("Unrecognized input! Please enter (y/n): ")
            stat_input = stat_input.lower()
        if trip:
            print('\n')
        return stat_input

    # Verifier for the (c/d) questions
    elif ver_code == 1:
        while ((stat_input != 'c') and (stat_input != 'd')):
            trip = True
            stat_input = input("Unrecognized input! Please enter (c/d): ")
            stat_input = stat_input.lower()
        if trip:
            print('\n')
        return stat_input

    # Verifier for the URL questions
    elif ver_code == 2:
        while (((stat_input[0:21]) != 'https://www.newegg.ca') or (
                (stat_input[-7:-1] + '1') != '&page=1')):
            print('\n')
            trip = True
            print('Please make sure that the URL is in the format:')
            print('https://www.newegg.ca/...&page=1')
            stat_input = input('Please try again: ')
        if trip:
            print('\n')
        return stat_input

    # Verifier for the input with 1, 2, or 3 as the options
    elif ver_code == 3:
        try:
            stat_input = int(stat_input)
            while ((stat_input != 1) and (
                    stat_input != 2) and (stat_input != 3)):
                trip = True
                stat_input = input(
                    'Unrecognized input! Please enter (1/2/3): ')
                try:
                    stat_input = int(stat_input)
                except:
                    trip = True
        except:
            while ((stat_input != 1) and (
                    stat_input != 2) and (stat_input != 3)):
                trip = True
                stat_input = input(
                    'Unrecognized input! Please enter (1/2/3): ')
                try:
                    stat_input = int(stat_input)
                except:
                    trip = True
        return stat_input

    # Verifier for the input when it needs to be an int
    elif ver_code == 5:
        try:
            stat_input = int(stat_input)
        except:
            while ((type(stat_input) is not int)):
                stat_input = input('Input needs to be an integer!: ')
                try:
                    stat_input = int(stat_input)
                except:
                    stat_input = 'a'
                if stat_input is int:
                    break
        return stat_input

    elif ver_code == 6:
        if stat_input < 1:
            stat_input = 1
        elif stat_input > 9:
            stat_input = 9
        return stat_input

    elif ver_code == 7:
        if stat_input < 1:
            stat_input = 1
        return stat_input
