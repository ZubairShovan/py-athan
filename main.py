import requests
import json
import time
import os
import logging
# import getch
import datetime as dt
from pygame import mixer
import playsound

logging.basicConfig(filename='logger.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

data = {}


def action(curr_time, salah, wait_time, is_fazr=False):
    mixer.init()  # Initialzing pyamge mixer

    if is_fazr is False:
        mixer.music.load('Sounds/azan1.mp3')  # Loading  File
    else:
        mixer.music.load('Sounds/fazrAzan.mp3')  # Loading  File

    cls()
    print(salah + " time started at " + curr_time)
    logging.info(salah + " time started at " + curr_time)
    mixer.music.play()

    # mixer.music.stop()

    # print("ESCAPE")
    time.sleep(60 * int(wait_time))
    logging.info("Resuming after break.")


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def isNowInTimePeriod(startTime, endTime, nowTime):
    if startTime < endTime:
        return nowTime >= startTime and nowTime <= endTime
    else:
        # Over midnight:
        return nowTime >= startTime or nowTime <= endTime


def update_time(mon, yr, latitude="43.768585", longitude="-79.503355"):
    # https://aladhan.com/prayer-times-api#GetCalendar
    cls()

    r = requests.get(
        'http://api.aladhan.com/v1/calendar?latitude='+latitude+'&longitude='+longitude+'&month=' + mon + '&year=' + yr + '&method=2&school=1')

    if str(r.status_code) != "200":
        logging.error("Request failed")
        return AssertionError("Request failed")
    else:

        # print(str(r.status_code))

        js = r.json()

        with open('content.txt', 'w') as convert_file:
            convert_file.write(json.dumps(js))

        print("Time is updating.")
        logging.info("Time has been updated.")
        time.sleep(3)


def read_data():
    global data

    with open('content.txt') as f:
        data = f.read()

    logging.info("Re-initialized the data.")


logging.info("App started.")

today = dt.date.today()
update_time(mon=today.strftime("%m"), yr=today.strftime("%Y"))

with open('content.txt') as f:
    data = f.read()


while True:
    today = dt.date.today()

    dc = json.loads(data)

    # Month abbreviation, day and year Sep-16-2019
    d = today.strftime("%d %b %Y")

    day = today.strftime("%d")
    month = today.strftime("%m")
    year = today.strftime("%Y")

    new_dict = dict()

    for a in dc["data"]:
        if a["date"]["readable"] == d:
            # print("READABLE: "+a["date"]["readable"])
            new_dict = a["timings"]
            # print(a["timings"])

    Fajr = new_dict['Fajr'].replace(" (EST)", ":00")
    Fajr1 = new_dict['Fajr'].replace(" (EST)", ":01")
    Fajr2 = new_dict['Fajr'].replace(" (EST)", ":02")

    Sunrise = new_dict['Sunrise'].replace(" (EST)", ":00")
    Sunrise1 = new_dict['Sunrise'].replace(" (EST)", ":00")
    Sunrise2 = new_dict['Sunrise'].replace(" (EST)", ":00")

    Dhuhr = new_dict['Dhuhr'].replace(" (EST)", ":00")
    Dhuhr1 = new_dict['Dhuhr'].replace(" (EST)", ":00")
    Dhuhr2 = new_dict['Dhuhr'].replace(" (EST)", ":00")

    Asr = new_dict['Asr'].replace(" (EST)", ":00")
    Asr1 = new_dict['Asr'].replace(" (EST)", ":00")
    Asr2 = new_dict['Asr'].replace(" (EST)", ":00")

    Sunset = new_dict['Sunset'].replace(" (EST)", ":00")

    Maghrib = new_dict['Maghrib'].replace(" (EST)", ":00")
    Maghrib1 = new_dict['Maghrib'].replace(" (EST)", ":00")
    Maghrib2 = new_dict['Maghrib'].replace(" (EST)", ":00")

    Isha = new_dict['Isha'].replace(" (EST)", ":00")
    Isha1 = new_dict['Isha'].replace(" (EST)", ":00")
    Isha2 = new_dict['Isha'].replace(" (EST)", ":00")

    Imsak = new_dict['Imsak'].replace(" (EST)", ":00")
    Midnight = new_dict['Midnight'].replace(" (EST)", ":00")


    now = dt.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    cls()
    print("Today is : " + d)
    print("Current Time is : ", current_time)
    print("")
    print("Fajr : " + Fajr)
    print("Sunrise : " + Sunrise)
    print("Dhuhr : " + Dhuhr)
    print("Asr : " + Asr)
    print("Maghrib : " + Maghrib)
    print("Isha : " + Isha)

    if current_time in (Fajr, Fajr1, Fajr2):
        action(current_time, "Fajr", 5, True)

    elif current_time in (Sunrise, Sunrise1, Sunrise2):
        print("It's " + current_time)
        print("Sunrise!")
        playsound.playsound('Sounds/Ding.mp3')

    elif current_time in (Dhuhr, Dhuhr1, Dhuhr2):
        action(current_time, "Dhuhr", 5, False)

    elif current_time in (Asr, Asr1, Asr2):
        action(current_time, "Asr", 5, False)

    elif current_time in (Maghrib, Maghrib1, Maghrib2):
        action(current_time, "Maghrib", 5, False)

    elif current_time in (Isha, Isha1, Isha2):
        action(current_time, "Isha", 5, False)

    elif current_time in ("00:00:00", "00:00:01", "00:00:02"):
        update_time(mon=month, yr=year)
        time.sleep(60)
        read_data()

    time.sleep(1)

# normal example:
# print(isNowInTimePeriod(dt.time(2,33), dt.time(3,30), dt.datetime.now().time()))


# print(dt.time(2,33))
