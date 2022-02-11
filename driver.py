'''
Webscraper created by Phillip Kluge.
This webscraper uses BeautifulSoup4 as a dependency,
make sure you have that and Python3 installed.

Please do not use this script too often as Newegg will detect
it as a DOS attack or a script; a VPN is recommended!

This is the driver code for newegg.py.
Please run the program using ./run if on Linux

Version: 2.1.0 R2
Current Release: 2022/02/10
Original Release: 2021/01/10

Github: @phillipkluge
LinkedIn: @phillipjkluge

This file conforms to the PEP-8 style guide.
'''

from newegg import Scraper
from newegg import input_verifier
from newegg import urllib

intel = ("https://www.newegg.ca/p/pl?N=100007670%2050001157&cm_sp="
         "Cat_CPU-Processors_8-_-Visnav-_-Intel-CPU&page=1")
amd = ("https://www.newegg.ca/p/pl?N=100007670%20601306869&cm_sp="
       "Cat_CPU-Processors_1-_-Visnav-_-AMD-CPU&page=1")


if __name__ == "__main__":

    debug = False
    state = input("Enable debug mode? (y/n): ")
    state = state.lower()
    state = input_verifier(0, state)
    if state == "y":
        debug = True
    else:
        debug = False

    print("\n")

    c_url = input("Change the default URL for Intel and AMD CPUs? "
                  "(Not recommended!) (y/n): ")
    c_url = c_url.lower()
    c_url = input_verifier(0, c_url)
    if c_url == "y":
        intel = input("Intel URL: ")
        intel = input_verifier(2, intel)

        amd = input("AMD URL: ")
        amd = input_verifier(2, amd)
    elif c_url == "n":
        print("No custom URL... continuing program execution")

    if debug:
        print("\n")
        print("------------------------DEBUG------------------------")
        print("Intel URL: " + intel)
        print("AMD URL: " + amd)
        print("-----------------------------------------------------")

    print("\n")

    scraper = Scraper(intel, amd, debug)

    error_trip = False
    try:
        scraper.scrape()
    except urllib.error.HTTPError:
        error_trip = True
        print("------ERROR------ERROR------ERROR------"
              "ERROR------ERROR------ERROR------ERROR------")
        print("INVALID URL! If using default the "
              "default URLs, consider changing them as they "
              "may be invalid")
        print("---------------------------------------"
              "--------------------------------------------")

    if debug and not error_trip:
        print("\n")
    elif not error_trip:
        print("Done!")
