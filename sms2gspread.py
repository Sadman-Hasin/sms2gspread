import sys
import colorama
from colorama import Fore, init
import subprocess
import json

import gspread


init(autoreset=True)


class Sms2gspread():
    def __init__(self, filename, sheet, number):
        self.print_message("Initiating Program..")
        self.file = filename
        self.wsheet = sheet
        self.number = number
        self.print_message(f"Attempting to Connect with Google Spreadsheet Name: {self.file} Sheet: {self.wsheet}.")
        self.service_account = gspread.service_account()
        self.sheet = self.service_account.open(self.file)
        self.worksheet = self.sheet.worksheet(self.wsheet)
        self.print_message("Connected Successfully!")

    def print_message(self, message):
        print(Fore.GREEN+"[MESSAGE]", message)

    def print_error(self, error):
        print(Fore.RED+"[ERROR]", error)

    def scrape_sms(self):
        out = subprocess.check_output([
            "termux-sms-list",
            "-f",
            self.number,
            "-l",
            "-1"
        ]).decode()

        sms = json.loads(out.replace("[", '{ "sms" : [').replace("]", "] }"))
        
        self.print_message(f"Collected SMS from {self.number}.")
        
        return sms

    def update_gspread(self):
        sms = self.scrape_sms()["sms"]

        self.print_message("Attempting to Update Google Spreadsheet.")
        for s in sms:
            self.worksheet.insert_row([
                s["number"],
                s["received"],
                s["body"]
            ], 2)

        self.print_message("Successfully Updated Google Spread Sheet!")

    
    def update_gspread_from_Dummy(self):
        raw_sms = """Tk3,935.00 received from A/C:019888656427 Fee:Tk0, Your A/C Balance: Tk7,125.69 TxnId:3513049767 Date:08-FEB-23 12:56:11 am. Download https://bit.ly/nexuspay"""
        values = [
                raw_sms[raw_sms.find("A/C:")+4:raw_sms.find("Fee:")-2],
                raw_sms[raw_sms.find("TxnId:")+6:raw_sms.find("Date")-1],
                raw_sms[2:raw_sms.find("received")-1],
                raw_sms[raw_sms.find("Date:")+5:raw_sms.find("Download")-2]
                ]

        self.worksheet.insert_row(values, 2)

        print("Updated Google Spread Sheet! (From Dummy Message)")




