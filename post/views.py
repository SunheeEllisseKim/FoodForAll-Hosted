import tweepy
import datetime
from django.conf import settings
from django.shortcuts import render, redirect
import requests
# Create your views here.

def CreateTweet(request):
        totalStr = ""
        if request.method == 'POST':
            content = request.POST.get('content', '')

            if content:
                print('Content', content)


                # auth = tweepy.OAuthHandler(settings.API_KEY, settings.API_KEY_SECRET)
                # auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
                # api = tweepy.API(auth)
                # api.update_status(content)
          

                # return redirect('index')
            #('DonationID', 'DonationName', 'DonationAllergies', 'DonationFoodBank', 'DonorEmail', 'DonorAddress', 'DonorZipCode', 'DonationQuantity')
            donationQuantity = 1
            
            DonationName = request.POST.get('DonationName', '')
            DonationExpirationDate = str(request.POST.get('DonationExpirationDate', ''))
            currDate = datetime.datetime.now().date()
            if DonationExpirationDate:
                tempCurrTime = int(currDate.strftime('%Y%m%d'))
                datetimeObj = datetime.datetime.strptime(DonationExpirationDate, "%Y-%m-%d").date()
                tempExpDate = int(datetimeObj.strftime('%Y%m%d'))
                print('DonationExpirationDate', DonationExpirationDate, "vs currtime", currDate)
                print('DonationExpirationDate2', DonationExpirationDate, "vs currtime", currDate, "currDate>DonationExpirationDate", (tempCurrTime>tempExpDate))
            if DonationName:
                print('DonationName', DonationName)
            DonationAllergies = request.POST.get('DonationAllergies', '')
            if DonationAllergies:
                print('DonationAllergies', DonationAllergies)
            donorEmail = request.POST.get('donorEmail', '')
            if donorEmail:
                print('donorEmail', donorEmail)
            donorAddr = request.POST.get('donorAddr', '')
            if donorAddr:
                print('donorAddr', donorAddr)
            donorZip = request.POST.get('donorZip', '')
            if donorZip:
                print('donorZip', donorZip)
            donationQuantity = request.POST.get('DonationQuantity', '')
            if donationQuantity:
                print('DonationQuantity', donationQuantity)

            foodbankVal = -999
            foodbankVal = findFoodBank(donorAddr, donorZip)

            URL = "https://tranquil-tundra-49633.herokuapp.com/donation"
  
            # location given here
            deptId = 1
            totalStr = ""
            
            if foodbankVal != -999 and DonationExpirationDate and (tempCurrTime<tempExpDate):
                if content:
                    print('Content', content)
                    client = tweepy.Client(consumer_key=settings.API_KEY, consumer_secret=settings.API_KEY_SECRET, access_token=settings.ACCESS_TOKEN, access_token_secret=settings.ACCESS_TOKEN_SECRET)
                    content = content + " just donated food!"
                    response = client.create_tweet(text=content)

                totalStr = "Successfully Uploaded Donation Entry"
                if DonationName == None or DonationName == "":
                    DonationName = "n/a"
                if DonationAllergies == None or DonationAllergies == "":
                    DonationAllergies = "n/a"
            
                if DonationName == None or DonationName == "":
                    DonationName = "n/a"
                if donorEmail == None or donorEmail == "":
                    donorEmail = "n/a"
                if donorAddr == None or donorAddr == "":
                    donorAddr = "n/a"
            
                if donorZip == None or donorZip == "":
                    donorZip = "n/a"
                if DonationExpirationDate == None or DonationExpirationDate == "":
                    DonationExpirationDate = "n/a"

                # defining a params dict for the parameters to be sent to the API "DepartmentName": "Support"
                myobj = {'DonationName':DonationName,  "DonationAllergies": DonationAllergies, "DonationFoodBank": str(foodbankVal),
            "DonorEmail": donorEmail, "DonorAddress": donorAddr,"DonorZipCode": donorZip, "DonationQuantity": donationQuantity, "DonationDeliveryStatus": False, "DonationDriver": "not assigned", "DonationExpirationDateStr": DonationExpirationDate}
                #addingDatabaseEntry(DonationName, DonationAllergies, foodbankVal, donorEmail, donorAddr, donorZip, donationQuantity)
                # sending get request and saving the response as response object
                
                r = requests.post(url = URL, json = myobj)
                print('r',r)
                r2 = requests.get(url = URL, params = {})
            
                # extracting data in json format
                data = r2.json()
                
                print('data',data)
            else:
                totalStr = "ERROR: Unable to upload donation entry - check address of donation pickup site or expiration date"

            


        # return
        return render(request,'post.html', {"FoodBankData": totalStr})

def findMatchingFoodBankDatabaseValue(foodbankName, foodbankAddr, foodBankPostalCode, foodBankCity):
    URL = "https://tranquil-tundra-49633.herokuapp.com/banks"
    print("+"*50)
    print('foodbankName', foodbankName)
    print('foodbankAddr', foodbankAddr)
    print('foodBankPostalCode', foodBankPostalCode)
    print('foodBankCity', foodBankCity)
    print("+"*50)
    # defining a params dict for the parameters to be sent to the API "DepartmentName": "Support"
    #myobj = {'DonationName':DonationName, "DonationName": DonationName, "DonationAllergies": DonationAllergies, "DonationFoodBank": "n/a",

    # sending get request and saving the response as response object
    #r = requests.post(url = URL, json = myobj)
    #print('r',r)
    r2 = requests.get(url = URL, params = {})
    returnedBanksList= r2.json()
    lastKnownIndex = -999
    for i in range(len(returnedBanksList)):
        lastKnownIndex = returnedBanksList[i]['FoodBankID']
        print("!"*50)
        print('foodbankName', returnedBanksList[i]['FoodBankName'], returnedBanksList[i]['FoodBankName'].strip()  == foodbankName.strip())
        print('FoodBankZipCode', returnedBanksList[i]['FoodBankZipCode'], " versus ", foodBankPostalCode, returnedBanksList[i]['FoodBankZipCode'].strip() == foodBankPostalCode.strip() )
        print('FoodBankCity', returnedBanksList[i]['FoodBankCity'])
        print('FoodBankAddress', returnedBanksList[i]['FoodBankAddress'], returnedBanksList[i]['FoodBankAddress'].strip() == foodbankAddr.strip())
        print("!"*50)
        if returnedBanksList[i]['FoodBankName'].strip()  == foodbankName.strip() and returnedBanksList[i]['FoodBankZipCode'].strip() == foodBankPostalCode.strip() and returnedBanksList[i]['FoodBankAddress'].strip() == foodbankAddr.strip():
            print("returnedBanksList[i]['FoodBankZipCode']",returnedBanksList[i]['FoodBankID'])
            return returnedBanksList[i]['FoodBankID']
            
    if foodBankPostalCode == "":
        foodBankPostalCode = "n/a"
    if foodBankCity == "":
        foodBankCity = "n/a"
    if foodbankName == "":
        foodbankName = "n/a"
    if foodbankAddr == "":
        foodbankAddr == "n/a"
    # if food bank details not already registered, must register them
    detailsOfFoodBank = {"FoodBankZipCode":foodBankPostalCode, "FoodBankCity": foodBankCity, "FoodBankName": foodbankName, "FoodBankAddress": foodbankAddr}
    #print("NO MATCH", detailsOfFoodBank)
    r = requests.post(url = URL, json = detailsOfFoodBank)
    #print(r)
    r3 = requests.get(url = URL, params = {})
    returnedBanksList= r2.json()
    # print(returnedBanksList)
    return (lastKnownIndex+1)

def returnJsonVal_FoodBankAPI(address, zip):
    try:
        addressStr = 'https://www.givefood.org.uk/api/2/locations/search/?address='+address+'&?postcode='+zip+'&?cause=Food Banks, Food Pantries, and Food Distribution'
        response = requests.get(addressStr)
        return response
    except requests.exceptions.HTTPError as error:
        return "error"
       
def findFoodBank(address, zip):
    #addressGeneralStr = 'https://www.givefood.org.uk/api/2/locations'
    #responseAllLocations = requests.get(addressGeneralStr)
    #allLocations = response.json()
    #for
    statusCode = returnJsonVal_FoodBankAPI(address, zip).status_code
    print("STATUS CODE",statusCode)
    if(statusCode == 200):
        addressStr = 'https://www.givefood.org.uk/api/2/locations/search/?address='+address+'&?postcode='+zip+'&?cause=Food Banks, Food Pantries, and Food Distribution'
        response = requests.get(addressStr)
        print("PRINT VIEWS response.json()",response.json())
        foodBanksDict = response.json()
        #print(foodBanksDict)
        #has 'postcode', 'district'
        covidAPILink = 'https://api.coronavirus.data.gov.uk/generic/code/postcode/'

        CollectedStr = ""
        CollectedArr = []
        CollectedDict = {} # key is food bank number (1-10) and value is an array of separated string - this is because new line is difficult to add to index
        
        foodbankName = foodBanksDict[0]['name']
        foodBankFirst = foodBanksDict[0]['address']
        foodBankFirstList = foodBankFirst.split("\r\n")
        foodbankaddr = ""
        foodbankCity = ""
        foodbankZip = ""

        if len(foodBankFirstList) > 1:
            foodbankaddr= foodBankFirstList[0]
        if len(foodBankFirstList) > 2:
            foodbankCity= foodBankFirstList[1]
        if len(foodBankFirstList) > 3:
            foodbankZip= foodBankFirstList[2]
        #foodbankCity = foodBanksDict[0]['city']
        foodbankZip = foodBanksDict[0]['postcode']
        print('foodbankCity', foodbankCity, 'foodbankZip', foodbankZip)
        foodbankID = -999
        foodbankID = findMatchingFoodBankDatabaseValue(foodbankName,foodbankaddr, foodbankZip, foodbankCity)
        return foodbankID
    return -999
    #print('foodBankFirst',foodBankFirstList)
    '''
    for i in range(len(foodBanksDict)):
        CollectedArr = []
        #CollectedStr = ""
        #print(response.json())
        covidResults = response.json()
        #print('i', fox[i])
        print('-'*50)
        CollectedStr = CollectedStr+"-"*50+"<br>"
        CollectedArr. append("-"*50+"<br>")
        print('Distance from location (meters):',str(foodBanksDict[i]['distance_m']))
        CollectedStr = CollectedStr+"<br>"+'Distance from location (meters):'+str(foodBanksDict[i]['distance_m'])+ "<br />"
        CollectedArr.append('Distance from location (meters):'+str(foodBanksDict[i]['distance_m']))
        print('Name of Charity/Food Bank: ', foodBanksDict[i]['name'])
        CollectedStr = CollectedStr+'Name of Charity/Food Bank: '+ foodBanksDict[i]['name']+ "<br />"
        print('Address of Charity/Food Bank: ', foodBanksDict[i]['address'])
        CollectedStr = CollectedStr+'Address of Charity/Food Bank: '+ foodBanksDict[i]['address'] + "<br />"
        #print('Website of Organization: ', foodBanksDict[i]['urls'])
        #print('District of Organization: ', foodBanksDict[i]['district'])
        postCode = foodBanksDict[i]['postcode']
        CollectedStr = CollectedStr+' Name of Charity/Food Bank: '+ foodBanksDict[i]['name'] + "<br />"
        CollectedArr.append('Name of Charity/Food Bank: '+ foodBanksDict[i]['name'])
        print('postcode of Organization: ', postCode)
        postCode = postCode.replace(' ', '%20')
        covidAPIStr = covidAPILink + postCode
        #print("covidAPIStr::::",covidAPIStr)
        covidAPIResponse = requests.get(covidAPIStr)
        utlaDataResults = covidAPIResponse.json()

        covidAPIStrResultingCases = 'https://api.coronavirus.data.gov.uk/generic/soa/utla/'+utlaDataResults['utla']+'/newCasesBySpecimenDate'

        covidAPIResponse2 = requests.get(covidAPIStrResultingCases)
        covidResults = covidAPIResponse2.json()
        print('Last known number of Covid Cases: ',covidResults['payload']['value'], " (date = "+covidResults['date']+")")
        
        covidLevel = covidResults['payload']['value']
        categoryOfLevel = ""
        if(float(covidLevel) < 20):
            categoryOfLevel = "LOW"
        elif (float(covidLevel) < 55):
            categoryOfLevel = "MEDIUM"
        else:
            categoryOfLevel = "HIGH"
        CollectedStr = CollectedStr + 'Covid Level ' + categoryOfLevel + " with "+str(covidResults['payload']['value'])+ " Cases (date = "+str(covidResults['date'])+")" + "<br />"
        print('REACH END OF COVID CASES')
        CollectedArr.append('Covid Level ' + categoryOfLevel + " with "+str(covidResults['payload']['value'])+ " Cases (date = "+str(covidResults['date'])+")")
    return CollectedStr
    '''
#findFoodBank("115 New Cavendish Street", "W1W 6UW")
#findFoodBank("45 Earlham Street", "WC2H 9LA")
#findFoodBank("17 Haverstock Hill Chalk Farm", "NW3 2BL") # issues with adding
#findFoodBank("Copenhagen Street Islington", "N1 0SR") ***** use
#findMatchingFoodBankDatabaseValue("Euston","St. Pancras Church House 1 Lancing Street", "NW1 1NA", "London")