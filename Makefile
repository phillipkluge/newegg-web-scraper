# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Webscraper created by Phillip Kluge.
# This webscraper uses BeautifulSoup4 as a dependency,
# make sure you have that and Python3 installed.
#
# Make sure that you do not use this too often as Newegg will detect
# it as a DOS attack or a script; a VPN is recommended!
#
# Version: 3.0.1 B1
# Current Release: 2022/02/14
# Original Release: 2021/01/10
#
# Github: @phillipkluge
# LinkedIn: @phillipjkluge
#
# This Makefile is meant to clean up any leftover outputs
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

clean:
	rm -rf __pycache__/ newegg.csv .~lock.newegg.csv#