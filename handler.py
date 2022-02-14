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

This file conforms to the PEP-8 style guide.
'''

import os
import sys
import shutil
from typing import Union
from time import sleep
from xmlrpc.client import Boolean, boolean
from constants import *

class Handler():

    @staticmethod
    def error_handler(type: Errors, exit: Boolean, delay: int) -> None:
        print(Formatting.ERROR_HEADER)
        if type == Errors.URL:
            print("INVALID URL; ERROR CODE: " + type)
        elif type == Errors.FILE:
            print("UNABLE TO OPEN FILE; ERROR CODE: " + type)
        elif type == Errors.LOAD:
            print("UNABLE TO LOAD PAGE; ERROR CODE: " + type)
        elif type == Errors.URL_SET:
            print("UNABLE TO SET URL; ERROR CODE: " + type)
        print(Formatting.ERROR_HEADER + "\n")

        sleep(delay)
        sys.exit(0)
    
    @staticmethod
    def input_handler(type: Inputs, stat_input: str, lower=0, upper=100) -> Union[str,int]:
        # Verifier for the (y/n) questions
        if type == Inputs.YES_NO:
            while True:
                if ((stat_input != "y") and (stat_input != "n")):
                    try:
                        stat_input = input("Unrecognized input! Please enter (y/n): ")
                        stat_input = stat_input.lower()
                    except SyntaxError:
                        continue
                    continue
                break
            return stat_input

        # Verifier for the URL questions
        elif type == Inputs.URL:
            while True:
                if ((stat_input[0:21] != "https://www.newegg.ca") or (
                        (stat_input[-7:-1] + "1") != "&page=1")):
                    print("Please make sure that the URL is in the format: \n"
                        "https://www.newegg.ca/...&page=1")
                    try:
                        stat_input = input("Please try again: ")
                    except SyntaxError:
                        continue
                    continue
                break
            return stat_input

        elif type == Inputs.NUMBER:
            while True:
                try:
                    stat_input = int(stat_input)
                except ValueError:
                    try:
                        stat_input = input("Please enter an integer: ")
                    except SyntaxError:
                        continue
                    continue

                if not (lower <= stat_input <= upper):
                    try:
                        stat_input = input("Please enter a valid number in range [" + str(lower) + "-" + str(upper) + "]: ")
                    except SyntaxError:
                        continue
                    continue
                break
            return stat_input
    
    @staticmethod
    def clean(done: Boolean=False) -> None:
        if not done:
            try:
                print("Cleaning up unfinished files... ",end='')
                os.remove("newegg.csv")
                print("done")
            except FileNotFoundError:
                print("none found")

        try:
            print("Cleaning up cache... ",end='')
            shutil.rmtree(path="./__pycache__/")
            print("done")
        except FileNotFoundError:
            print("none found")
