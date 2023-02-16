import sys
import time
import colorama
from colorama import Fore, init

from sms2gspread import Sms2gspread

init(autoreset=True)


def main():
    while True:
        try:
            sms = Sms2gspread(
                filename="School Fess 2023",
                sheet="RocketPayment",
                number="16216",
            )                                                     
        
            sms.main()
    
        except Exception as e:
            print(Fore.RED+"[ERROR]", e)
            for seconds in list(range(1, 11))[::-1]:
                print(Fore.YELLOW+f"[RESTART] Restarting Program in {seconds} second(s)...")
                time.sleep(1)


main()
