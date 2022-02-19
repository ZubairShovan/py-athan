import requests
import json


def update_time(mon, year):
    # mon (str): 8 or 08 for August.
    # year (str): 2022

    r = requests.get(
            'http://api.aladhan.com/v1/calendar?latitude=43.768585&longitude=-79.503355&month='+mon+'&year='+year+'&method=2&school=1')

    if str(r.status_code) != "200":
        AssertionError("Request failed")
    else:

        # print(str(r.status_code))

        js = r.json()
        print(type(js))

        with open('content.txt', 'w') as convert_file:
            convert_file.write(json.dumps(js))


update_time(mon="2", year="2022")
