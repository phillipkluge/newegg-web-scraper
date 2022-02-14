'''
Webscraper created by Phillip Kluge.
This webscraper uses BeautifulSoup4 as a dependency,
make sure you have that and Python3 installed.

Make sure that you do not use this too often as Newegg will detect
it as a DOS attack or a script; a VPN is recommended!

Version: 3.0.1 B1
Current Release: 2022/02/14
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
    MODULE = 4


class Inputs(Enum):
    YES_NO = 0  # If input is a yes/no question
    URL = 1  # If input needs to be a URL
    NUMBER = 2  # If input needs to be in an int and in a certain range


class Formatting():
    PROGRAM_VERSION: str = ("3.0.1 B1")
    HEADER_LENGTH: int = 10
    PROGRAM_HEADER: str = ("-----" * HEADER_LENGTH)
    ERROR_HEADER: str = ("=====" * HEADER_LENGTH)


def print_header() -> None:
    print(Formatting.PROGRAM_HEADER)
    print("NEWEGG WEB SCRAPER")
    print("Author: Phillip Kluge")
    print("Github: @phillipkluge")
    print("Running version: " + Formatting.PROGRAM_VERSION)
    print(Formatting.PROGRAM_HEADER)
