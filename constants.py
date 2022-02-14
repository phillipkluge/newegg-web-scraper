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

This file conforms to the PEP-8 style guide.'''

from enum import Enum

class Errors(Enum):
    URL = 0
    FILE = 1
    LOAD = 2
    URL_SET = 3

class Inputs(Enum):
    YES_NO = 0  # If input is a yes/no question
    URL = 1  # If input needs to be a URL
    NUMBER = 2  # If input needs to be in an int and in a certain range

class Formatting():
    HEADER_LENGTH: int=8
    PROGRAM_HEADER: str=("-----" * HEADER_LENGTH)
    ERROR_HEADER: str=("*****" * HEADER_LENGTH)

    
