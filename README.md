# newegg-web-scraper
______________________________
Author: Phillip Kluge
Email: phillipjkluge@gmail.com
Github: @phillipkluge
______________________________

The main function of the program is to scrape Newegg for CPUs, although it can be used on other products as well (like graphics cards)
The format of the URL MUST be compatible. (i.e. must be in the format 'https://www.newegg.ca/...&page=1'; see default URLs below for an example)

The program comes with preset URLs for Intel and AMD CPUs that has been tested to function on day of release, although you are free to change them if they no longer work, just
enter 'y' when it asks "Change the default URL for Intel and AMD CPUs? (Not recommended!) (y/n):". If the default URLs not longer work, please contact me and I will update them.

If you wish to scrape another Newegg URL (even if they're not related to CPUs), input 'c' when the program asks "Enter a CUSTOM link for scraping, or use DEFAULTS? (c/d):", then enter the desired URL.
(keeping in mind that the format must be 'https://www.newegg.ca/...&page=1')


-Current default Intel CPU URL: https://www.newegg.ca/p/pl?N=100007670%2050001157&cm_sp=Cat_CPU-Processors_8-_-Visnav-_-Intel-CPU&page=1

-Current default AMD CPU URL: https://www.newegg.ca/p/pl?N=100007670%20601306869&cm_sp=Cat_CPU-Processors_1-_-Visnav-_-AMD-CPU&page=1

***Dependencies:
	
	-Please make sure that you have Python 3.8+ and BeautifulSoup 4.0+ installed in order for this to work. You can run it with the run.bat
	 file if you're on Windows or by simply executing the 'newegg.py' file with a Python 3.8+ interperator.

	-Use "sudo apt-get install python3-bs4" to install BeautifulSoup4 if on Linux.

***Output:
	
	-The output will be placed into a .csv file. Program may take 30+ seconds depending on CPU speed, internet speed, and any delay entered, although internet connection is 	 the main bottleneck.

***Important Notes:
	
	-Make sure that you do not use this program too often; Newegg will detect it as a bot. You will likely get an error
	 if that happens. For this reason I HIGHLY recommend a VPN, so you can switch servers if the program starts to encounter errors.

	-You can add a delay between each page being evaluated. While this works really well in reducing the number of errors,
	 it also DRAMATICALLY increases the execution time, as after each page it waits the specified number of seconds before moving on to the next.
	 
	-If you encounter any issues, please contact me. I am also aware that the code is very messy and inefficient; this being a byproduct of updating old code to new standards,

***Included Files:
	
	-newegg.py
	-README.md
	-run.bat
	
***Outputs:
	
	-newegg.csv
