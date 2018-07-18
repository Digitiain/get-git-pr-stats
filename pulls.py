
import config
import requests

from datetime import datetime, timedelta


def main():
    parameters = {"state": config.PR_STATE}
    request_url = "https://api.github.com/repos/" + config.REPO_URL_SUFFIX + "/pulls"
    response = requests.get(request_url, params=parameters)
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

    convert_merged_at_to_datetime_object(listofmerges)


def convert_merged_at_to_datetime_object(listofmerges):

    convertedmerges = []

    print("Converting Github's date format to one that can be compared with today's datetime...")

    for merge in listofmerges:
        convertedmerges.append(datetime.strptime(str(merge), '%Y-%m-%dT%H:%M:%SZ')) # Original output looks like this: 2018-07-17T15:54:49Z

    get_recent_merges(convertedmerges)


def get_recent_merges(listofmerges):

    today = datetime.now()

    finalnumberofmerges = 0
    daydiff = config.NUM_DAYS_AGO

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
