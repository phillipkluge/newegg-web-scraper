'''
Webscraper created by Phillip Kluge.
This webscraper uses BeautifulSoup4 as a dependency,
make sure you have that and Python3 installed.

Please do not use this script too often as Newegg will detect
it as a DOS attack or a script; a VPN is recommended!

This is the driver code for newegg.py.
Please run the program using ./run if on Linux

Version: 3.0.1 B1
Current Release: 2022/02/14
Original Release: 2021/01/10

Github: @phillipkluge
LinkedIn: @phillipjkluge

This file conforms to the PEP-8 style guide.
'''

import urllib
import signal
import sys
from newegg import Scraper
from handler import Handler
from constants import Errors, print_header

intel = ("https://www.newegg.ca/p/pl?N=100007670%2050001157&cm_sp="
         "Cat_CPU-Processors_8-_-Visnav-_-Intel-CPU&page=1")
amd = ("https://www.newegg.ca/p/pl?N=100007670%20601306869&cm_sp="
       "Cat_CPU-Processors_1-_-Visnav-_-AMD-CPU&page=1")


def signal_handler(sig, frame):
    print("\nABORTING PROGRAM...")
    sys.exit(0)


if __name__ == "__main__":
    print_header()

    signal.signal(signal.SIGINT, signal_handler)

    handler = Handler()
    scraper = Scraper(intel, amd)

    try:
        scraper.scrape()
        print("\n" + "Done!")
    except urllib.error.HTTPError:
        handler.error_handler(type=Errors.LOAD, exit=True, delay=3)
