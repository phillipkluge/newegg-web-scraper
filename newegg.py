'''
Webscraper created by Phillip Kluge. This webscraper uses BeautifulSoup4 as a dependency, make sure you have that and Python3 installed.
Make sure that you do not use this too often as Newegg will detect it as a DOS attack or a script; a VPN is recommended!

Version: 2.0.0 R1
Release: 2021/01/10

Github: @phillipkluge
LinkedIn: @phillipjkluge
Twitter: @phillipjkluge

'''

# importing all necessary dependencies
import urllib
from urllib.request import urlopen as urlreq
from bs4 import BeautifulSoup as bsoup
import csv
import datetime
from time import sleep

class Scraper:
    def __init__(self, intel, amd, debug):
        #Sets the target URL
        self.intel = intel
        self.amd = amd
        self.debug = debug
        self.delay = 0

        cpu_setting = input('Enter a CUSTOM link for scraping, or use DEFAULTS? (c/d): ')
        cpu_setting = cpu_setting.lower()
        cpu_setting = input_verifier(1, cpu_setting)
        if cpu_setting == 'd':
            num_setting = input('Press 1 for the Intel URL, 2 for the AMD, or 3 for both: ')
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
            self.page_limit = input('Max number of pages: ')
            self.page_limit = input_verifier(5, self.page_limit)
            self.page_limit = input_verifier(7, self.page_limit)
        elif page_setting == 'n':
            self.page_limit = -1

        print('\n')

        ask_delay = input('Add a delay between each page? May reduce proliferation of errors. (y/n): ')
        ask_delay = ask_delay.lower()
        ask_delay = input_verifier(0, ask_delay)
        if ask_delay == 'y':
            delay_in = input('Delay (in seconds) (1-9) : ')
            delay_in = input_verifier(5, delay_in)
            delay_in = input_verifier(6, delay_in)
            self.delay = delay_in
        else:
            print('No delay specified... continuing program execution')

        print('\n')

        self.first = True

        try:
            num_setting = int(num_setting)
            if num_setting == 1:
                self.target_url = intel
                self.repeat = False

            elif num_setting == 2:
                self.target_url = amd
                self.repeat = False

            elif num_setting == 3:
                self.target_url = intel
                self.repeat = True
        except:
            self.target_url = num_setting
            self.repeat = False

    def scrape(self):
        if self.first:
            titles = "brand, product_name, sale_percentage, price, shipping, total, url_link"
            file_name = "newegg.csv"
            try:
                f = open(file_name, "w")
            except PermissionError:
                print("------ERROR------ERROR------ERROR------ERROR------ERROR------ERROR------ERROR------")
                print("FILE OPEN ERROR! Please close the .csv file before running the program.")
                print("-----------------------------------------------------------------------------------")
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
                print("------ERROR------ERROR------ERROR------ERROR------ERROR------ERROR------ERROR------")
                print("FILE OPEN ERROR! Please close the .csv file before running the program.")
                print("-----------------------------------------------------------------------------------")
                print('\n')
                print("Exiting program...")
                sleep(3)
                quit()

        # setting the target URL, downloading the page, reading the contents, and dumping it into a variable called url_page_dump
        url_page_download = urlreq(self.target_url)
        url_page_dump = url_page_download.read()
        url_page_download.close()

        # parses the dumped page into html
        page_soup = bsoup(url_page_dump, "html.parser")

        # finds the total number of pages
        try:
            num_of_pages = (page_soup.find_all("span", {"class":"list-tool-pagination-text"}))[0].strong.text[2:]
        except:
            num_of_pages = '1'

        if self.debug:
            print('------------------------------DEBUG------------------------------')
        # looping through all the found pages
        for i in range(1, int(num_of_pages) + 1):
            if ((i > self.page_limit) & (self.page_limit != -1)):
                break

            if i == self.page_limit:
                page_limit_test = True
            else:
                page_limit_test = False

            digit_length = len(str(i - 1))
            self.target_url = self.target_url[0:-digit_length] + str(i)
            if self.debug:
                print('PAGE URL: ' + str(self.target_url))

            url_page_download = urlreq(self.target_url)
            url_page_dump = url_page_download.read()
            page_soup = bsoup(url_page_dump, "html.parser")



            try:
                anchor_element = page_soup.find("div", {"class":"list-tool-search"}).label.text
                if anchor_element != "Search Within:":
                    print("\n")
                    print("------ERROR------ERROR------ERROR------ERROR------ERROR------ERROR------ERROR------")
                    print("Newegg has likely detected this as a bot! Please consider adding a delay, limiting")
                    print("pages, and changing the VPN server location!")
                    print("-----------------------------------------------------------------------------------")
                    print("\n")
                    print("Exiting program...")
                    sleep(3)
                    quit()
            except AttributeError:
                print("\n")
                print("------ERROR------ERROR------ERROR------ERROR------ERROR------ERROR------ERROR------")
                print("Newegg has likely detected this as a bot! Please consider adding a delay, limiting")
                print("pages, and changing the VPN server location!")
                print("-----------------------------------------------------------------------------------")
                print("\n")
                print("Exiting program...")
                sleep(3)
                quit()

            # finds every product listing on the current page
            item_containers = page_soup.find_all("div", {"class":"item-container"})
            #print(len(item_containers))

            #loops through all the products (container) and returns useful information about them
            for container in item_containers:
                if self.debug:
                    print('PAGE: ' + str(i))
            
                # finds the product brand
                try:
                    product_brand = container.find("a", {"class":"item-brand"}).img["title"]
                except:
                    product_brand = 'Unknown Brand'
                if self.debug:
                    print('BRAND: ' + product_brand)

                # finds the product name
                try:
                    product_name = container.find("a", {"class":"item-title"}).text
                except:
                    product_name = "Unknown Name"
                if self.debug:
                    print('PRODUCT NAME: ' + product_name)


                # finds the sale percentage
                try:
                    product_sale_percent = container.find("span", {"class":"price-save-percent"}).text
                    if product_sale_percent[-1] != "%":
                        product_sale_percent = "0%"
                except:
                    product_sale_percent = "0%"
                if self.debug:
                    print('SALE PERCENT: ' + product_sale_percent)

                # finds the product price and replaces a comma with nothing if there exists one in the price
                try:
                    product_price_dollars = container.find("li", {"class":"price-current"}).strong.text
                    product_price_cents = container.find("li", {"class":"price-current"}).sup.text
                    product_price = (product_price_dollars + product_price_cents)
                except:
                    product_price = "0"
                if ("," in product_price):
                    product_price = product_price.replace(",", "")
                if self.debug:
                    print('PRICE: ' + product_price)

                # finds the product shipping price
                try:
                    product_shipping_price = container.find("li", {"class":"price-ship"}).text
                except:
                    product_shipping_price = "0"
                if (product_shipping_price == ""):
                    product_shipping_price = "0"
                elif (product_shipping_price[0] == "$"):
                    product_shipping_price = product_shipping_price[1:product_shipping_price.find(" ")]
                elif (product_shipping_price == "Free Shipping"):
                    product_shipping_price = "0"
                else:
                    product_shipping_price = "0"
                if self.debug:
                    print('SHIPPING PRICE: ' + product_shipping_price)

                # calculates the total product price with shipping included (also limits the float value to 2 decimal places)
                try:
                    total_product_price = '%.2f' % (float(product_price) + float(product_shipping_price))
                    if (total_product_price == "0"):
                        total_product_price = 'Unknown Price'
                except:
                    total_product_price = product_price
                if self.debug:
                    print('TOTAL PRICE: ' + total_product_price)

                try:
                    product_link = container.find("a", {"class":"item-title"})["href"]
                except:
                    product_link = 'https://newegg.ca'
                if self.debug:
                    print('URL: ' + product_link)

                f.write(product_brand + "," + product_name.replace(",", ";") + "," + product_sale_percent + "," + product_price + "," + product_shipping_price + "," \
                    + total_product_price + "," + product_link + "\n")
                if self.debug:
                    print('_____________________________________________________')

            if ((self.delay != 0) & (i != int(num_of_pages)) & (page_limit_test == False)):
                if self.debug:
                    print('\n')
                    print('------------------------DEBUG------------------------')
                    print('Delaying for ' + str(self.delay) + ' second(s)')
                    print('-----------------------------------------------------')

                for i in range(0, self.delay):
                    if self.debug:
                        print('Delay time left: ' + str(self.delay - i), end="\r")
                    sleep(1)

                if self.debug:
                    print('\n')
                    print('_____________________________________________________')

        if self.debug:
            print('-----------------------------------------------------------------')
            print('\n')
            print('------------------------DEBUG------------------------')
            print('End of main sequence reached!')
            print('-----------------------------------------------------')

        f.close()

        if self.repeat:
            if self.debug:
                print('\n')
                print('------------------------DEBUG------------------------')
                print('Repeat sequence reached!')
                print('-----------------------------------------------------')
                print('\n')
            self.repeat = False
            self.first = False

            self.target_url = amd

            self.scrape()

def input_verifier(ver_code, stat_input):
    #Verifier for the (y/n) questions
    trip = False
    if ver_code == 0:
        while ((stat_input != 'y') and (stat_input != 'n')):
            trip = True
            stat_input = input("Unrecognized input! Please enter (y/n): ")
            stat_input = stat_input.lower()
        if trip:
            print('\n')
        return stat_input

    #Verifier for the (c/d) questions
    elif ver_code == 1:
        while ((stat_input != 'c') and (stat_input != 'd')):
            trip = True
            stat_input = input("Unrecognized input! Please enter (c/d): ")
            stat_input = stat_input.lower()
        if trip:
            print('\n')
        return stat_input

    #Verifier for the URL questions
    elif ver_code == 2:
        while (((stat_input[0:21]) != 'https://www.newegg.ca') or ((stat_input[-7:-1] + '1') != '&page=1')):
            print('\n')
            trip = True
            #print(stat_input[0:21])
            #print(stat_input[-7:-1] + '1')
            print('Please make sure that the URL is in the format:')
            print('https://www.newegg.ca/...&page=1')
            stat_input = input('Please try again: ')
        if trip:
            print('\n')
        return stat_input

    #Verifier for the input with 1, 2, or 3 as the options
    elif ver_code == 3:
        try:
            stat_input = int(stat_input)
            while ((stat_input != 1) and (stat_input != 2) and (stat_input != 3)):
                trip = True
                stat_input = input('Unrecognized input! Please enter (1/2/3): ')
                try:
                    stat_input = int(stat_input)
                except:
                    trip = True
        except:
            while ((stat_input != 1) and (stat_input != 2) and (stat_input != 3)):
                trip = True
                stat_input = input('Unrecognized input! Please enter (1/2/3): ')
                try:
                    stat_input = int(stat_input)
                except:
                    trip = True
        return stat_input

    #Verifier for the input when it needs to be an int
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


if __name__ == "__main__":
    debug = False

    state = input('Enable debug mode? (y/n): ')
    state = state.lower()
    state = input_verifier(0, state)
    if state == 'y':
        debug = True
    else:
        debug = False

    print('\n')

    intel = 'https://www.newegg.ca/p/pl?N=100007670%2050001157&cm_sp=Cat_CPU-Processors_8-_-Visnav-_-Intel-CPU&page=1'
    amd = 'https://www.newegg.ca/p/pl?N=100007670%20601306869&cm_sp=Cat_CPU-Processors_1-_-Visnav-_-AMD-CPU&page=1'

    c_url = input('Change the default URL for Intel and AMD CPUs? (Not recommended!) (y/n): ')
    c_url = c_url.lower()
    c_url = input_verifier(0, c_url)
    if c_url == 'y':
        intel = input('Intel URL: ')
        intel = input_verifier(2, intel)

        amd = input('AMD URL: ')
        amd = input_verifier(2, amd)
    elif c_url == 'n':
        print('No custom URL... continuing program execution')

    if debug:
        print('\n')
        print('------------------------DEBUG------------------------')
        print('Intel URL: ' + intel)
        print('AMD URL: ' + amd )
        print('-----------------------------------------------------')

    print('\n')

    scraper_1 = Scraper(intel, amd, debug)
    error_trip = False
    try:
        scraper_1.scrape()
    except urllib.error.HTTPError:
        error_trip = True
        print('------ERROR------ERROR------ERROR------ERROR------ERROR------ERROR------ERROR------')
        print('INVALID URL! If using default the default URLs, consider changing them as they')
        print('may be invalid')
        print('-----------------------------------------------------------------------------------')


    if debug and not error_trip:
        print('\n')
    elif not error_trip:
        print('Done!')