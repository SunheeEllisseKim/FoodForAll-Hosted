
#from asyncio.windows_events import NULL
import requests

def returnJsonVal_FoodBankAPI(address, zip):
    try:
        addressStr = 'https://www.givefood.org.uk/api/2/locations/search/?address='+address+'&?postcode='+zip+'&?cause=Food Banks, Food Pantries, and Food Distribution'
        response = requests.get(addressStr)
        return response
    except requests.exceptions.HTTPError as error:
        return "error"

def returnDataForRecipient(address, zip):
    print('reached returnDataForRecipient')
    #address = '115 New Cavendish Street'#input('Enter Address of Pickup:\n') #115 New Cavendish Street example location

    #address2 = '12 Millbank, Westminster, London SW1P 4QE'
    statusCode = returnJsonVal_FoodBankAPI(address, zip).status_code
    print("STATUS CODE",statusCode)
    if(statusCode == 200):
        addressStr = 'https://www.givefood.org.uk/api/2/locations/search/?address='+address+'&?postcode='+zip+'&?cause=Food Banks, Food Pantries, and Food Distribution'
        #print("addrStr", addressStr)
        response = requests.get(addressStr)
        #print("addr Response", response)
        #print(response.json())
        foodBanksDict = response.json()
        #print(foodBanksDict)
        #has 'postcode', 'district'
        covidAPILink = 'https://api.coronavirus.data.gov.uk/generic/code/postcode/'

        CollectedStr = ""
        CollectedArr = []
        CollectedDict = {} # key is food bank number (1-10) and value is an array of separated string - this is because new line is difficult to add to index
        for i in range(len(foodBanksDict)):
            CollectedArr = []
            #CollectedStr = ""
            #print(response.json())
            covidResults = response.json()
            #print('i', fox[i])
            #print('-'*50)
            print('-'*50)
            CollectedStr = CollectedStr+"-"*50+"<br>"
            CollectedArr. append("-"*50+"<br>")
            print('Distance from location (meters):',str(foodBanksDict[i]['distance_m']))
            CollectedStr = CollectedStr+"<br>"+'       Distance from location (meters):'+str(foodBanksDict[i]['distance_m'])+ "<br />"
            CollectedArr.append('Distance from location (meters):'+str(foodBanksDict[i]['distance_m']))
            print('Name of Charity/Food Bank: ', foodBanksDict[i]['name'])
            CollectedStr = CollectedStr+'       Name of Charity/Food Bank: '+ foodBanksDict[i]['name']+ "<br />"
            print('Address of Charity/Food Bank: ', foodBanksDict[i]['address'])
            CollectedStr = CollectedStr+'       Address of Charity/Food Bank: '+ foodBanksDict[i]['address'] + "<br />"#print('Website of Organization: ', foodBanksDict[i]['urls'])
            #print('District of Organization: ', foodBanksDict[i]['district'])
            postCode = foodBanksDict[i]['postcode']
            CollectedStr = CollectedStr+'       Name of Charity/Food Bank: '+ foodBanksDict[i]['name'] + "<br />"
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
            CollectedStr = CollectedStr + '       Covid Level ' + categoryOfLevel + " with "+str(covidResults['payload']['value'])+ " Cases (date = "+str(covidResults['date'])+")" + "<br />"
            print('REACH END OF COVID CASES')
            CollectedArr.append('Covid Level ' + categoryOfLevel + " with "+str(covidResults['payload']['value'])+ " Cases (date = "+str(covidResults['date'])+")")

            foodbankName = foodBanksDict[i]['name']
            foodBankFirst = foodBanksDict[i]['address']
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
            print("******foodbankID", foodbankID)
            if foodbankID!= -999:
                #CollectedStr = CollectedStr + "<<<<<Donations Available>>>>>" +"<br />"
                URL_donations = "https://tranquil-tundra-49633.herokuapp.com/donation"
                r_don = requests.get(url = URL_donations, params = {})
                returnedDonationList = r_don.json()
                print(len(returnedDonationList))
                for indexV in range(len(returnedDonationList)):
                    #print('first fb', str(returnedDonationList[indexV]["DonationFoodBank"]).strip(), 'second fb', foodbankID, str(returnedDonationList[indexV]["DonationFoodBank"]).strip()  == str(foodbankID).strip())
                    #print('delivery status', (returnedDonationList[indexV]["DonationDeliveryStatus"]))

                    if str(returnedDonationList[indexV]["DonationFoodBank"]).strip()  == str(foodbankID).strip() and (returnedDonationList[indexV]["DonationDeliveryStatus"]  == True or returnedDonationList[indexV]["DonationDeliveryStatus"] is None):
                        CollectedStr = CollectedStr + "            - Donation Name: "+ returnedDonationList[indexV]["DonationName"] +"<br />"
                        CollectedStr = CollectedStr + "            - Donation Allergies: "+ returnedDonationList[indexV]["DonationAllergies"]+"<br />"
                        CollectedStr = CollectedStr + "            - Donation Quantity: "+ str(returnedDonationList[indexV]["DonationQuantity"])+"<br />"
                        CollectedStr = CollectedStr +"<br />"
    else:
        CollectedStr = "ERROR: Address and Zipcode Entry Invalid"
        

    return CollectedStr
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
            
 
    return -999

'''
def returnDatabaseDonationsFromFoodBank():

    #first find which zip code and  food bank name matches food donor
    # using the foodbankID will then use donationToFoodBank to view the donationID vals
    #using donationID vals will take the matching donation
   

    
    URL_FindBankID = "https://tranquil-tundra-49633.herokuapp.com/banks"


    # api-endpoint
    URL = "https://tranquil-tundra-49633.herokuapp.com/department"
    
    # location given here
    deptId = 1

    # defining a params dict for the parameters to be sent to the API "DepartmentName": "Support"
    myobj = {'DepartmentName':"testadd"}
    
    # sending get request and saving the response as response object
    r = requests.post(url = URL, json = myobj)
    print('r',r)
    r2 = requests.get(url = URL, params = {})
    # extracting data in json format
    data = r2.json()
    
    print('data',data)
'''

def returnDataForTransport(postCode):
    
    #address = '115 New Cavendish Street'#input('Enter Address of Pickup:\n') #115 New Cavendish Street example location
    postCode = postCode.replace(' ', '%20')
    #NW1 8YS -> NW1208YS
    #SE1 8TY (postcode by foodbank)
    #1) receive UTLA value from covid API for conversion from postcode
    covidAPILink = 'https://api.coronavirus.data.gov.uk/generic/code/postcode/'
    covidAPIStr = covidAPILink + postCode
    covidAPIResponse = requests.get(covidAPIStr)
    utlaDataResults = covidAPIResponse.json()

    # retrieve the general coronovirus data from this postcode
    covidAPIStrResultingCases = 'https://api.coronavirus.data.gov.uk/generic/soa/utla/'+utlaDataResults['utla']+'/newCasesBySpecimenDate'

    covidAPIResponse2 = requests.get(covidAPIStrResultingCases)
    covidResults = covidAPIResponse2.json()
    #print('covidResults', covidResults)

    #print('Last known number of Covid Cases: ',covidResults['payload']['value'], " (date = "+covidResults['date']+")")
        
    covidLevel = covidResults['payload']['value']
    categoryOfLevel = ""
    if(float(covidLevel) < 20):
        categoryOfLevel = "LOW"
    elif (float(covidLevel) < 55):
        categoryOfLevel = "MEDIUM"
    else:
        categoryOfLevel = "HIGH"

    CollectedStr ='Covid Level ' + categoryOfLevel + " with "+str(covidResults['payload']['value'])+ " Cases (date = "+str(covidResults['date'])+")" + "<br />"
    print(CollectedStr)
    return CollectedStr
    
#returnDataForTransport('NW1 8YS')
#returnDataForRecipient("115 New Cavendish Street")

#print(fox[0]['distance_m'])
#from __future__ import division, unicode_literals 
'''
print()
print()
with open('index.html') as f:
  print(f.read())



from bs4 import BeautifulSoup
with open('index.html', 'r') as f:

    contents = f.read()

    soup = BeautifulSoup(contents, 'lxml')

    print(f'HTML: {soup.head},  text: {soup.body}')

import os
import time
 
# Insert the directory path in here
path = os.getcwd()
 
# Extracting all the contents in the directory corresponding to path
l_files = os.listdir(path)
 
# Iterating over all the files
for file in l_files:
   
  # Instantiating the path of the file
    file_path = f'{path}\\{file}'
 
    # Checking whether the given file is a directory or not
    if os.path.isfile(file_path):
        try:
            # Printing the file pertaining to file_path
            os.startfile(file_path, 'print')
            print(f'Printing {file}')
 
            # Sleeping the program for 5 seconds so as to account the
      # steady processing of the print operation.
            time.sleep(5)
        except:
            # Catching if any error occurs and alerting the user
            print(f'ALERT: {file} could not be printed! Please check\
            the associated softwares, or the file type.')
    else:
        print(f'ALERT: {file} is not a file, so can not be printed!')
         
print('Task finished!')

soup = BeautifulSoup(open('index.html'), 'html.parser')

print('soup', soup)
p_tag = soup.new_tag("p")
p_tag.string = 'This is the new paragraph'

with open("index.html", "r") as file:
    print(file.read())
from bs4 import BeautifulSoup
soup = BeautifulSoup(open('index.html'), 'html.parser')

print('soup', soup)
p_tag = soup.new_tag("p")
p_tag.string = 'This is the new paragraph'

with open("index.html", "r") as file:
    print(file.read())

soup = BeautifulSoup(fileName, 'html.parser')
if soup != None and soup != NULL:
    soup.body.insert(0, 'here reached')
print(soup)

fileOpenWrite = open('index.html', 'w')

from bs4 import BeautifulSoup
soup = BeautifulSoup(fileName, 'html.parser')
print('soup', soup)
p_tag = soup.new_tag("p")
p_tag.string = 'This is the new paragraph'
if(soup != None):
    soup.body.append(p_tag)
with fileOpenWrite as file:
    file.write(str(soup))
'''
