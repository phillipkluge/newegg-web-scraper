'''
Webscraper created by Phillip Kluge. This webscraper uses BeautifulSoup4 as a dependency, make sure you have that and Python3 installed.
Make sure that you do not use this too often as Newegg/Amazon/Memeory-Express will detect it as a DOS attack or a script, dont go overboard ;)
Don't change the URL given below as that may break some things. If any site has updated their website and this script no longer works, contact me.
Make sure all version are the same between Python files, otherwise things could break. Keep all python files in the same folder.

I recommend a VPN to make sure you're not treated as a bot right away. If you get an out of index error, that's where that's from. Sorry, switch locations.

Version: 1.0.0

Github: @phillipkluge
LinkedIn: @phillipjkluge
Twitter: @phillipjkluge

'''
# checking all the newegg CPUs
import newegg
intel_url = 'https://www.newegg.ca/p/pl?N=100007670%2050001157&cm_sp=Cat_CPU-Processors_8-_-Visnav-_-Intel-CPU&page=1'
amd_url = 'https://www.newegg.ca/p/pl?N=100007670%20601306869&cm_sp=Cat_CPU-Processors_1-_-Visnav-_-AMD-CPU&page=1'
newegg.scraper(intel_url)
newegg.scraper(amd_url)