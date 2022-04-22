from django.shortcuts import render
# from requests import post
import requests
#from foodbank.models import Donation, FoodBanks, banks
import json
from django.http import HttpResponseRedirect
# Create your views here.

def DonationsForBank(userinput):
    print("made it to donations for bank")
    URL = "https://tranquil-tundra-49633.herokuapp.com/banks"
    r2 = requests.get(url = URL, params = {})
    returnedBanksList= r2.json()
    # print("----"*10)
    # print(returnedBanksList) --> untitled1
    # print(len(returnedBanksList)) --> 9
    # print(type(returnedBanksList)) --> list
    # # country_dict = json.loads(returnedBanksList[0]) --> dict
    # print(type(returnedBanksList[0]))
    for i in range(len(returnedBanksList)):
        foodbankName = returnedBanksList[i]['FoodBankName']
        print("Checking foodbank: ",foodbankName)
        if (foodbankName == userinput):
            print("found the foodbank")
            #found the foodbank the employee was searching in banks
            foodbankID = returnedBanksList[i]['FoodBankID']
            print("foodbank id:", foodbankID)
            URL = "https://tranquil-tundra-49633.herokuapp.com/donation"
            r3 = requests.get(url = URL, params = {})
            returnedDonationsList= r3.json()
            listOfDonations = []
            for j in range(len(returnedDonationsList)):
                donationFoodBank = returnedDonationsList[j]['DonationFoodBank']
                print("Checking donation's foodbank: ",donationFoodBank)
                print("returnedDonationsList[j]['DonationDeliveryStatus']", returnedDonationsList[j]['DonationDeliveryStatus'])
                print("donationFoodBank == str(foodbankID)", donationFoodBank == str(foodbankID))
                if (donationFoodBank == str(foodbankID) and returnedDonationsList[j]['DonationDeliveryStatus'] == False):
                    print("donation foodbank matches")
                    listOfDonations.append(returnedDonationsList[j])
            return listOfDonations
    
    return False #could not find food bank
    


    # qs = banks.objects.filter(FoodBankName__text_search=userinput)
    # print(qs)

    # foodbank = banks.object.get(FoodBankName=userinput)
    # print("FOODBANK:", foodbank)
    # foodbankid = foodbank.FoodBankID

    # queryset = Donation.objects.filter(DonationFoodBank=foodbankid)

def testPutFunction():
    x = {'DonationID': '55', 'DonationName': 'chicken legs', 'DonationAllergies': 'n/a', 'DonationFoodBank': '9', 'DonorEmail': 'final@gmail.com', 'DonorAddress': '114 New Cavendish Street', 'DonorZipCode': 'W1W 6UW', 'DonationQuantity': '6', 'DonationDeliveryStatus': 'true', 'DonationDriver': 'John Doe'}
    URL2 = "https://tranquil-tundra-49633.herokuapp.com/donation"
    y = {
        "DonationID": 55,
        "DonationName": "chicken legs EDITED",
        "DonationAllergies": "n/a",
        "DonationFoodBank": "9",
        "DonorEmail": "final@gmail.com",
        "DonorAddress": "114 New Cavendish Street",
        "DonorZipCode": "W1W 6UW",
        "DonationQuantity": 6,
        "DonationDeliveryStatus": True,
        "DonationDriver": "not assigned EDITEd"
    }        
    r4 = requests.put(url = URL2, json=[x])
    print(r4.status_code)
    print('finished')
def drivers(request):
    context=''
    if request.method == 'POST':
        userinput = request.POST.get('FoodBankName')
        deliveriesList = request.POST.get('DeliveryName')
        driverName = request.POST.get('DriverName')
        deliveryBank = request.POST.get('DeliveryBank')
        if userinput:
            print("USER INPUT: ", userinput)
            queryset = DonationsForBank(userinput)
            print('queryset', queryset)
            if queryset == False:
                #couldn't find food bank
                found = 'not found'
                context = {'contentVal':"food bank not registered in database"}
                return render(request, 'drivers.html', context)
            elif (len(queryset) == 0):
                #no donations for that food bank
                context = {'contentVal':"no donations for that food bank"}
                return render(request, 'drivers.html', context)
            else:
                pretty = json.dumps(queryset[0], indent=4)
                print("=========="*13)
                # print(type(pretty))
                ToPrint = ""
                for k in range(len(queryset)):
                    print('k', k)
                    ToPrint += (json.dumps(queryset[k], indent=4) + '\n\n')
                context = {'contentVal':ToPrint}
                return render(request, 'drivers.html', context)
        
        deliveryBank = request.POST.get('DeliveryBank')
        deliveriesList = request.POST.get('DeliveryName')
        driverName = request.POST.get('DriverName')
        print('deliveryBank', deliveryBank, '\tdeliveriesList', deliveriesList, '\tdriverName', driverName)
        if deliveryBank or deliveriesList or driverName:
            if deliveryBank == "" or deliveryBank == None:
                deliveryBank = "n/a"
            if deliveriesList == "" or deliveriesList == None:
                deliveriesList = "n/a"
            if driverName == "" or driverName == None:
                driverName = "n/a"
  
            queryset = DonationsForBank(deliveryBank)
            if queryset == False:
                found = 'not found'
                context = {'contentVal':"food bank not registered in database"}
                return render(request, 'drivers.html', context)
            elif (len(queryset) == 0):
                #no donations for that food bank
                context = {'contentVal':"no donations for that food bank - deliveries not marked"}
                return render(request, 'drivers.html', context)
            else:
                URL2 = "https://tranquil-tundra-49633.herokuapp.com/donation"
                requestedList = deliveriesList.split(', ')
                for k in range(len(queryset)):
                    for j in range(len(requestedList)):
                        print('requestedList[j]', requestedList[j], ' queryset[k]',  queryset[k],(requestedList[j] == queryset[k]) )
                        if(requestedList[j] == str(queryset[k]['DonationID'])):
                            ToPrint = "Successful Upload for Donation ID"+str(queryset[k]['DonationID'])
                            newParams = queryset[k]
                            newParams['DonationDriver']= driverName
                            newParams['DonationDeliveryStatus']=True
                            print('newParams', newParams)
                            r4 = requests.put(url = URL2, data = newParams)
                            #returnedDonationsList= r4.json()
                context = {'contentVal':ToPrint}
                return render(request, 'drivers.html', context)
                

                            

                   
                


         



        # if queryset:
        #     string = ""
        #     for i in queryset:
        #         string += (str(i)+'\n')
        #     context = {'string':string}

        #     return render(request, 'drivers.html', context)
        # else:
        #     context = {'string':"no donations found"}
        #     return render(request, 'drivers.html', context)
        # context = {'string':"rip"}
        # return render(request, 'drivers.html', context)
    else:
        context = {'string':"string"}
    
    return render(request, 'drivers.html', context)
#testPutFunction()

