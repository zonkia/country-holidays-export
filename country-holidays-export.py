import requests
from pprint import pprint
import os
import time
import json

os.chdir(os.path.dirname(__file__))

apiKey = "[YOUR API KEY]"
acceptable_formats = ["TXT", "JSON"]
holidaysMenu = {1: "All", 2: "National holiday", 3: "Observance", 4: "Season"}

def save_chosen_holidays_to_file(holidayChoice, dataJsonHolidays, formatChoice):
    if formatChoice == "JSON":
        with open("Holidays.json", "w", encoding="UTF-8-sig") as holidaysFile:
            holidaysDict = {}
            if holidayChoice != "All":
                for holidays in dataJsonHolidays["response"]["holidays"]:
                    if holidays["type"][0] == holidayChoice:
                        holidaysDict[holidays["date"]["iso"]] = str(holidays["name"]) + ": " + str(holidays["description"])
                json.dump(holidaysDict, holidaysFile, ensure_ascii=False, indent=4)
                return holidaysDict
            else:
                for holidays in dataJsonHolidays["response"]["holidays"]:
                    holidaysDict[holidays["date"]["iso"]] = str(holidays["type"]) + ", " + str(holidays["name"]) + ": " + str(holidays["description"])
                json.dump(holidaysDict, holidaysFile, ensure_ascii=False, indent=4)
                return holidaysDict
    elif formatChoice == "TXT":
        with open("Holidays.txt", "w", encoding="UTF-8-sig") as holidaysFile:
            holidaysDict = {}
            if holidayChoice != "All":
                for holidays in dataJsonHolidays["response"]["holidays"]:
                    if holidays["type"][0] == holidayChoice:
                        holidaysDict[holidays["date"]["iso"]] = str(holidays["name"]) + ": " + str(holidays["description"])
                holidaysFile.write("All [" + holidayChoice + "] holidays in " + countryName + " in " + str(year) + "\n"+ "\n")
                for entry in holidaysDict:
                    holidaysFile.write(entry + " " + holidaysDict[entry] + "\n"+ "\n")
                return holidaysDict
            else:
                for holidays in dataJsonHolidays["response"]["holidays"]:
                    holidaysDict[holidays["date"]["iso"]] = str(holidays["type"]) + ", " + str(holidays["name"]) + ": " + str(holidays["description"])
                holidaysFile.write("All holidays in " + countryName + " in " + str(year) + "\n"+ "\n")
                for entry in holidaysDict:
                    holidaysFile.write(entry + " " + holidaysDict[entry] + "\n"+ "\n")
                return holidaysDict

# check country name and get country code
parametersCountryCode_dict = {
                            "api_key": apiKey
                            }

dataJsonCountries = requests.get("https://calendarific.com/api/v2/countries", parametersCountryCode_dict).json()

while True:
    countryName = input("Please enter country name: ").title()
    try:
        for country in dataJsonCountries["response"]["countries"]:
            if country["country_name"] == countryName:
                countryCode = country["iso-3166"]
        if countryCode == "":
            continue
        else:
            print(countryName, "- country code:", countryCode)
            break
    except:
        print("Wrong country name, please try again")
        print()
        continue

# get JSON with holidays for country/year
while True:
    try:
        year = int(input("Please enter year: "))
        if len(list(str(year))) == 4:
            break
        else:
            print("Wrong year, please try again")
            continue
    except:
        print("Wrong year, please try again")
        continue

parametersHolidays_dict = {
                            "api_key": apiKey,
                            "year": year,
                            "country": countryCode
                            }

dataJsonHolidays = requests.get("https://calendarific.com/api/v2/holidays", parametersHolidays_dict).json()

# choose holiday type for export
print()
while True:
    holidayNoChoice = int(input("""Please choose holiday type:
1. All
2. National holiday
3. Observance
4. Season
"""))
    if holidayNoChoice in range(1, 5):
        holidayChoice = holidaysMenu[holidayNoChoice]
        break
    else:
        print("Wrong choice, please try again")
        time.sleep(1)
        print()
        continue
print(holidayChoice)
print()

#choose export format TXT or JSON
while True:
    formatChoice = input("Please choose your format: TXT or JSON: ").upper()
    if formatChoice in acceptable_formats:
        break
    else:
        print("Wrong format, please try again")
        continue

holidaysPrint = save_chosen_holidays_to_file(holidayChoice, dataJsonHolidays, formatChoice) # run function and export files

#pretty printer
print()
printChoice = input("Do you want to show the holidays export in this window? YES/NO").upper()
if printChoice == "YES":
    pprint(holidaysPrint)
else:
    print("Goodbye")
    time.sleep(3)
    os.close