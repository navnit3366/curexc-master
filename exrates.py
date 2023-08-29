
import urllib3.request
import sys
import json
import os
import csv
import codecs
import datetime

#URL used to fetch the data
currenciesJSONurl="http://openexchangerates.org/api/currencies.json"
ratesJSONurl="http://openexchangerates.org/api/historical/{0}.json?app_id={1}"

#output folder name
dataFolderName="data"

#getting the app ID fromthe appropriate file
def getAppID():
    try:
        #reading the app-ID file
        appIDfile = open('app.id')
        rawID = appIDfile.read()
    except FileNotFoundError:
        #in case the file is missing
        sys.stderr("Error: App ID file is missing")
        sys.exit(-17)
    except:
        sys.stderr("Error: couldn't open the app id file")
        sys.exit(-17)

    #stripping the app ID from the possibly serrounding white spaces
    return rawID.strip(' \t\n\r')

#custom exception of missing currency
class CurrencyDoesntExistError(Exception):
    pass


#data folder check- used before writing the files
def outputFolderCheck():
    #check if the data folder exists
    if not os.path.exists(dataFolderName):
        try:
            #creating the data folder
            os.mkdir(dataFolderName)
        except OSError:
            print("Error: couldn't create the output folder")
            sys.exit()


#getting infromation from ta specific URL
def getDataFromURL(url):
    #creating a request for the URL
    try:
        http = urllib3.PoolManager()
        req = http.request('GET', url)
        decodedResp=req.data.decode('utf-8')

    except urllib3.exceptions:
        print("URL is not valid")
        sys.exit()


    try:
        #the actual convertion from the response to a dictionary
        jsonDictionary = json.loads(decodedResp)
    except ValueError:
        #if the convertion to the dictionary failed
        print("Error: the JSON corrupted")
        sys.exit()

    return jsonDictionary

#getting the currencies list from the web
def _fetch_currencies():
    return getDataFromURL(currenciesJSONurl)

#getting the rates list from the web
def _fetch_exrates(date):
    # get the raw data
    ratesData = getDataFromURL(ratesJSONurl.format(date,appID))

    try:
        #getting the rates section of the json
        ratesList = ratesData['rates']
    except KeyError:
        #in case the 'rates' section is missing
        print("json format isn't valid")
        sys.exit()

    return ratesList


#saving currencies to a file
def _save_currencies(currencies):
    #create the data folder if it's not already existing
    outputFolderCheck()

    try:
        #create the currencies file
        currenciesFile=codecs.open(os.path.join(dataFolderName, "currencies.csv"), 'w','utf-8')
    except IOError:
        print("Error: couldn't create the currencies file")
        sys.exit()

    writer = csv.writer(currenciesFile)
    #writing the header
    writer.writerow(["Code", "Name"])

    #writing all the currencies
    for code, name in currencies.items():
        writer.writerow([code, name])

    #closing the file
    currenciesFile.close()
    return

#saving the rates to a file
def _save_exrates(date, rates):
    # create the data folder if it's not already existing
    outputFolderCheck()

    try:
        #create the rates file
        ratesFile=codecs.open(os.path.join(dataFolderName, "rates-"+date+".csv"), 'w','utf-8')
    except IOError:
        print("Error: couldn't create the rates file")
        sys.exit()

    writer = csv.writer(ratesFile)
    # writing the header
    writer.writerow(["Code", "Rate"])

    # writing all the currencies
    for code, rate in rates.items():
        writer.writerow([code, rate])

    # closing the file
    ratesFile.close()
    return


#parse the csv input file and returns dictionary correlated to the file
def parseCSVfile(csvFile):
    # initializing dictionary
    dict = {}

    # reading the file as a csv
    genericCSVfile = csv.reader(csvFile, delimiter=',')
    for line in genericCSVfile:
        dict[line[0]] = line[1]

    return dict

#loading the currencies from a file
def _load_currencies():
    try:
        # opening the input file
        with codecs.open(os.path.join(dataFolderName, "currencies.csv"),'r','utf-8') as currenciesFile:
            #parse the raw csv file data to a dictionary
            currenciesList = parseCSVfile(currenciesFile)
            currenciesFile.close()
    except FileNotFoundError:
        raise
    except IOError:
        print("error reading the file")
        sys.exit()


    return currenciesList

#loading the rates from a file
def _load_exrates(date):
    try:
        # opening the input file
        with open(os.path.join(dataFolderName, "rates-"+date+".csv")) as ratesFile:
            # parse the raw csv file data to a dictionary
            ratesList = parseCSVfile(ratesFile)
            ratesFile.close()
    except FileNotFoundError:
        raise
    except IOError:
        print("error reading the file")
        sys.exit()

    return ratesList

#get the currencies- if an appropriate fiel doesn't exist- fetch data from the web
def get_currencies():
    try:
        #load currencies from a file
        loadedCurrencies=_load_currencies()
    except FileNotFoundError:
        #getting the currencies list from the web
        loadedCurrencies=_fetch_currencies()

        #saving the currencies list in the appropriate file
        _save_currencies(loadedCurrencies)

    return loadedCurrencies

#get the rates- if an appropriate file doesn't exist- fetch data from the web
def get_exrates(date):
    try:
        # load rates from a file
        loadedRates=_load_exrates(date)
    except FileNotFoundError:
        #getting the rates list from the web
        loadedRates=_fetch_exrates(date)

        #saving the rates list in the appropriate file
        _save_exrates(date, loadedRates)

    return loadedRates

#convert amount of money from one currency to another based on the rates for a specific day
def convert(amount, from_curr, to_curr, date=""):
    #if the date is missing- relate it as today's date
    if(date==""):
        date=datetime.date.today()

    #getting the rates for the date from the web
    ratesList = _fetch_exrates(date)

    try:
        #calculate the result
        result=amount*ratesList[to_curr]/ratesList[from_curr]
    except KeyError:
        #if one of the currencies rate is missing for the requested day
        raise CurrencyDoesntExistError("The currency used in the conversion is missing")

    return result

#getting the app ID from the file
appID=getAppID()


