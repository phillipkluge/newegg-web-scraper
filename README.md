# Newegg Web Scraper
______________________________
Author: Phillip Kluge \
Email: phillipjkluge@gmail.com \
Github: @phillipkluge \
Version: 2.1.0 R1 \
Current Release: 2022/02/10 \
Original Release: 2021/01/10
______________________________

# Overview and Function
The main function of the program is to scrape Newegg for CPUs, although it can be used on other products as well (like graphics cards).
The format of the URL __MUST__ be compatible. (i.e. must be in the format `https://www.newegg.ca/...&page=1`; see default URLs below for an example).

The program comes with preset URLs for Intel and AMD CPUs that has been tested to function on day of release, although you are free to change them if they no longer work, just enter `y` when it asks `Change the default URL for Intel and AMD CPUs? (Not recommended!) (y/n):`.
If the default URLs not longer work, please contact me and I will update them.

If you wish to scrape another Newegg URL (even if they're not related to CPUs), input `c` when the program asks `Enter a CUSTOM link for scraping, or use DEFAULTS? (c/d):` (keeping in mind that the above format).

Default Intel CPU URL:
> https://www.newegg.ca/p/pl?N=100007670%2050001157&cm\_sp=Cat\_CPU-Processors\_8-\_-Visnav-\_-Intel-CPU&page=1


Default AMD CPU URL:
> https://www.newegg.ca/p/pl?N=100007670%20601306869&cm\_sp=Cat\_CPU-Processors\_1-\_-Visnav-\_-AMD-CPU&page=1

## Dependencies:
	
* Please make sure that you have Python 3.8+ and BeautifulSoup 4.0+ installed in order for this to work.
* Use `$ sudo apt install python3-bs4` to install BeautifulSoup4 if on Debian based Linux.

## Running the Program:

* Extract all files and move into that directory.
* Do `$ chmod +x ./run`.
* Then use `$ ./run` to execute the program in a terminal window.

## Output:
	
* The output will be placed into a .csv file. Program may take 30+ seconds depending on CPU speed, internet speed, and any delay entered, although internet connection is the main bottleneck.

## Important Notes:
	
* Make sure that you do not use this program too often; Newegg will detect it as a bot. You will likely get an error if that happens. For this reason I HIGHLY recommend a VPN, so you can switch servers if the program starts to encounter errors.

* You can add a delay between each page being evaluated. While this works really well in reducing the number of errors, it also DRAMATICALLY increases the execution time, as after each page it waits the specified number of seconds before moving on to the next.

* If you encounter any issues, please contact me. I am also aware that the code is very messy and inefficient; this being a byproduct of updating old code to new standards.

## Included Files:
	
* newegg.py
* README.md
* run
	
## Outputs:
	
* newegg.csv

## JAN 2022 UPDATE NOTES:

* Updated some of the code for better practice; including the addition of some comments.
* Both the `driver.py` and the `newegg.py` files were updated to conform with PEP-8 standards.
* .bat script was changed out for a shell script in order to run on Linux. If you don't like this change you are more than welcome to message me and I will ignore it.

## PLANNED UPDATES:

* Refactor the code in such a way as to embrace a more "object-oriented" approach; remove unnecessary lines and shrink file size.
* Bug fixes:
    * Item information is placed in the wrong .csv column (likely due to a website update).

###### Please note that this code is relatively old and has some bad programming practices throughout. With a proper refactoring, it could probably be sped up signficantly. 

###### If something does not work I would not be suprised. You can email me and I will try to get it fixed, although, with how out of date this code is, there are no guarantees.
