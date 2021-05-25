import os
from datetime import datetime, date, timedelta
import calendar
import time

def crawl():
    # os.system('python schedule/for_schedule.py') # Running Crawl File

    '''test'''
    now = str(datetime.now().minute)
    with open('schedule/a.txt', 'a') as f:
        f.write(now + '\n')

def first_monday_of_the_month(now): # Crawling on each First Monday of the month
    month_range = calendar.monthrange(now.year, now.month)
    delta = (calendar.MONDAY - month_range[0]) % 7
    # date_corrected = date(now.year, now.month, 1)
    # first_monday = date_corrected + timedelta(days = delta)
    if not delta:
        return True
    return False

def schedule_crawl():
    while True:
        now = datetime.now()
        if not first_monday_of_the_month(now):  # 'not' for test 
                                                # because day of test this function is not the fisrt MONDAY of the month:v
                                                # remove it if scheduling for project
            crawl()                            
            time.sleep(5) # 24*3600 Checking day by day


if __name__ == '__main__':
    schedule_crawl()
