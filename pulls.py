
import json
import requests
import time

from datetime import datetime, timedelta


def main():
    parameters = {"state": "closed"}
    response = requests.get("https://api.github.com/repos/alphagov/re-build-systems/pulls", params=parameters)
    if response.status_code == 200:
        print("Response successful with status code 200")
    else:
        print("Uh oh! Response unsuccessful with status code " + str(response.status_code))
        print("Aborting. So long cruel w...")

    data = response.json()

    merged = 0
    unmerged = 0
    listofmerges = []

    print("Getting list of dates on which pull requests were merged...")
    print("Ignoring unmerged pull requests...")
    for i in data:
        if i['merged_at'] is not None:
            merged += 1
            listofmerges.append(i['merged_at'])
        else:
            unmerged += 1

    # print("There have been " + str(merged) + " pull requests merged.")
    # print("There have been " + str(unmerged) + " pull requests that weren't merged.")

    convert_merged_at_to_datetime_object(listofmerges)


def convert_merged_at_to_datetime_object(listofmerges):

    convertedmerges = []

    print("Converting Github's date format to one that can be compared with today's datetime...")
    for merge in listofmerges:
        # print("Old merge: ")
        # print(merge)
        # print(type(merge))
        convertedmerges.append(datetime.strptime(str(merge), '%Y-%m-%dT%H:%M:%SZ')) # Original output looks like this: 2018-07-17T15:54:49Z
    #     print("New merge: ")
    #     print(merge)
    #     print(type(merge))
    # print(convertedmerges)

    get_recent_merges(convertedmerges)


def get_recent_merges(listofmerges):

    today = datetime.now()
    twoweeksago = timedelta(days=14)

    finalnumberofmerges = 0
    daydiff = 14

    print("Counting the number of merges that have happened in the last " + str(daydiff) + " days...")
    for merge in listofmerges:
        if (today - merge) < timedelta(daydiff):
            finalnumberofmerges += 1
        else:
            pass

    print("")
    print("")
    print("In the last " + str(daydiff) + " days there have been " + str(finalnumberofmerges) + " merged pull requests.")
    print("")


if __name__ == '__main__':
    main()
