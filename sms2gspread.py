import sys
import time
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
        
        self.new_sms = []
        self.timeInterval = 1

    def print_message(self, message):
        print(Fore.GREEN+"[MESSAGE]", message)

    def print_error(self, error):
        print(Fore.RED+"[ERROR]", error)

    def checkNewMessages(self, all_sms, i=-1):
        new = self.scrape_sms(i*(-1))["sms"][i]
        if not new["body"] == all_sms[-1]["body"] :
            self.new_sms.append(new)

            self.checkNewMessages(all_sms, i-1)

        

    def scrape_sms(self, l=-1):
        out = subprocess.check_output([
            "termux-sms-list",
            "-f",
            self.number,
            "-l",
            str(l)
        ]).decode()

        sms = json.loads(out.replace("[", '{ "sms" : [').replace("]", "] }"))
         
        return sms

    def formatBodySMS(self, body):
        values = [
                body[body.find("A/C:")+4:body.find("Fee:")-2],
                body[body.find("TxnId:")+6:body.find("Date")-1],
                body[2:body.find("received")-1],
                body[body.find("Date:")+5:body.find("Download")-2]
            ]

        return values

    def update_gspread(self, values): 
        self.worksheet.insert_row(values, 2)
    
    def main(self):
        sms = self.scrape_sms()["sms"]
        self.print_message(f"Collected SMS from {self.number}.")
        
        self.print_message("Attempting to Update Google Spreadsheet.")

        for s in sms:
            sms_body = s["body"]
            values = self.formatBodySMS(sms_body)

            if not self.worksheet.find(values[1]):
                self.update_gspread(values)

        self.print_message("Successfully Updated Google Spread Sheet!")
        
        self.print_message(f"Started Listening for New SMS with time interval of {self.timeInterval} seconds.")
        while True:
            self.checkNewMessages(sms)
            if self.new_sms:
                for s in self.new_sms[::-1]:
                    values = self.formatBodySMS(s["body"])
                    if not self.worksheet.find(values[1]):
                        self.update_gspread(values)

                        self.print_message("Successfully Updated Google Spread Sheet!")
                
                    sms.append(s)

                self.new_sms = []

            
            time.sleep(self.timeInterval)





