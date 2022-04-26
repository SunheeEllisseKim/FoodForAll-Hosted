from django.shortcuts import render, redirect
# from requests import post
import requests
#from foodbank.models import Donation, FoodBanks, banks
import json
from django.http import HttpResponseRedirect
import datetime
import pandas as pd
# Create your views here.

def DonationsForBank(userinput):
    print("made it to donations for bank")
    URL = "https://tranquil-tundra-49633.herokuapp.com/banks"
    r2 = requests.get(url = URL, params = {})
    returnedBanksList= r2.json()

    for i in range(len(returnedBanksList)):
        foodbankName = returnedBanksList[i]['FoodBankName']
        # print("Checking foodbank: ",foodbankName)
        if (foodbankName == userinput):
            #found the foodbank the employee was searching in banks
            foodbankID = returnedBanksList[i]['FoodBankID'] #associated foodbank id for the food bank employee works at
            # print("foodbank id:", foodbankID)
            URL = "https://tranquil-tundra-49633.herokuapp.com/donation"
            r3 = requests.get(url = URL, params = {})
            returnedDonationsList= r3.json()
            listOfDonations = []
            for j in range(len(returnedDonationsList)):
                donationFoodBank = returnedDonationsList[j]['DonationFoodBank'] #DonationFoodBank: food bank id
                # print("Checking donation's foodbank: ",donationFoodBank)
                # print("returnedDonationsList[j]['DonationDeliveryStatus']", returnedDonationsList[j]['DonationDeliveryStatus'])
                # print("donationFoodBank == str(foodbankID)", donationFoodBank == str(foodbankID))
                if (donationFoodBank == str(foodbankID) and returnedDonationsList[j]['DonationDeliveryStatus'] == False):
                    # print("donation foodbank matches")
                    DonationExpirationDate = str(returnedDonationsList[j]["DonationExpirationDateStr"]).strip() 
                
                    currDate = datetime.datetime.now().date()
                    #print('1currdate', currDate, 'DonationExpirationDate', DonationExpirationDate)
                    #if DonationExpirationDate == None or DonationExpirationDate == "":
                        #print('3currdate', currDate, 'DonationExpirationDate', DonationExpirationDate)
                    if DonationExpirationDate != "None":
                        #print('2currdate', currDate, 'DonationExpirationDate', DonationExpirationDate)
                        #print()
                        tempCurrTime = int(currDate.strftime('%Y%m%d'))
                        datetimeObj = datetime.datetime.strptime(DonationExpirationDate, "%Y-%m-%d").date()
                        tempExpDate = int(datetimeObj.strftime('%Y%m%d'))
                        #print('DonationExpirationDate', DonationExpirationDate, "vs currtime", currDate)
                        #print('DonationExpirationDate2', DonationExpirationDate, "vs currtime", currDate, "currDate>DonationExpirationDate", (tempCurrTime>tempExpDate))
                        if  (tempCurrTime<tempExpDate):

                            listOfDonations.append(returnedDonationsList[j])
            return listOfDonations
    
    return False #could not find food bank
    


    # qs = banks.objects.filter(FoodBankName__text_search=userinput)
    # print(qs)

    # foodbank = banks.object.get(FoodBankName=userinput)
    # print("FOODBANK:", foodbank)
    # foodbankid = foodbank.FoodBankID

    # queryset = Donation.objects.filter(DonationFoodBank=foodbankid)

# def testPutFunction():
#     x = {'DonationID': '55', 'DonationName': 'chicken legs', 'DonationAllergies': 'n/a', 'DonationFoodBank': '9', 'DonorEmail': 'final@gmail.com', 'DonorAddress': '114 New Cavendish Street', 'DonorZipCode': 'W1W 6UW', 'DonationQuantity': '6', 'DonationDeliveryStatus': 'true', 'DonationDriver': 'John Doe'}
#     URL2 = "https://tranquil-tundra-49633.herokuapp.com/donation"
#     y = {
#         "DonationID": 55,
#         "DonationName": "chicken legs EDITED",
#         "DonationAllergies": "n/a",
#         "DonationFoodBank": "9",
#         "DonorEmail": "final@gmail.com",
#         "DonorAddress": "114 New Cavendish Street",
#         "DonorZipCode": "W1W 6UW",
#         "DonationQuantity": 6,
#         "DonationDeliveryStatus": True,
#         "DonationDriver": "not assigned EDITEd"
#     }        
#     r4 = requests.put(url = URL2, json=y)
#     print(r4.status_code)
#     print('finished')
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
                # found = 'not found'
                context = {'contentVal':"food bank not registered in database"}
                return render(request, 'drivers.html', context)
            elif (len(queryset) == 0):
                #no donations for that food bank
                context = {'contentVal':"no donations for that food bank"}
                return render(request, 'drivers.html', context)
            else:
                # pretty = json.dumps(queryset[0], indent=4)
                # # print("=========="*13)
                # # print(type(pretty))
                # ToPrint = ""
                # for k in range(len(queryset)):
                #     print('k', k)
                #     ToPrint += (json.dumps(queryset[k], indent=4) + '\n\n')
                # context = {'contentVal':ToPrint}
                request.session['OpenDonations'] = queryset
                df = pd.DataFrame(queryset)
                dfg = df.groupby(['DonationID','DonationName','DonationAllergies','DonationFoodBank','DonorEmail','DonorAddress','DonorZipCode','DonationQuantity','DonationDeliveryStatus','DonationDriver']).sum()
                ToPrint = dfg.to_html()
                ToPrint = ToPrint.replace("DonationID","ID",1)
                ToPrint = ToPrint.replace("DonationName","Food",1)
                ToPrint = ToPrint.replace("DonationAllergies","Allergies",1)
                ToPrint = ToPrint.replace("DonationFoodBank","FoodBank",1)
                ToPrint = ToPrint.replace("DonorEmail","Donor Email",1)
                ToPrint = ToPrint.replace("DonorAddress","Donor Address",1)
                ToPrint = ToPrint.replace("DonorAddress","Zip Code",1)
                ToPrint = ToPrint.replace("DonationQuantity","Quantity",1)
                ToPrint = ToPrint.replace("DonationDeliveryStatus","Delivery Status",1)
                ToPrint = ToPrint.replace("DonationDriver","Driver",1)
                    
                # ToPrint = ""
                # for k in range(len(possibleDonations)):
                #     ToPrint += (json.dumps(possibleDonations[k], indent=4) + '\n')
                context = {'contentVal':ToPrint}
                #return redirect('takeadonation')
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
                            r4 = requests.put(url = URL2, json = newParams)
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
def drivers2(request):

    if request.method == 'POST':
        userinput = request.POST.get('FoodBankName')
        
        if userinput:
            print("USER INPUT: ", userinput)
            queryset = DonationsForBank(userinput)
            print('queryset', queryset)
            if queryset == False:
                #couldn't find food bank
                # found = 'not found'
                context = {'contentVal':"food bank not registered in database"}
                return render(request, 'drivers.html', context)
            elif (len(queryset) == 0):
                #no donations for that food bank
                context = {'contentVal':"no donations for that food bank"}
                return render(request, 'drivers.html', context)
            else:
                # pretty = json.dumps(queryset[0], indent=4)
                # # print("=========="*13)
                # # print(type(pretty))
                # ToPrint = ""
                # for k in range(len(queryset)):
                #     print('k', k)
                #     ToPrint += (json.dumps(queryset[k], indent=4) + '\n\n')
                # context = {'contentVal':ToPrint}
                request.session['OpenDonations'] = queryset
                return redirect('takeadonation')
                # return render(request, 'drivers.html', context)
        else:
            context = {'contentVal':"please input a food bank name"}

        # deliveryBank = request.POST.get('DeliveryBank')
        # deliveriesList = request.POST.get('DeliveryName')
        # driverName = request.POST.get('DriverName')
        # print('deliveryBank', deliveryBank, '\tdeliveriesList', deliveriesList, '\tdriverName', driverName)
        # if deliveryBank or deliveriesList or driverName:
        #     if deliveryBank == "" or deliveryBank == None:
        #         deliveryBank = "n/a"
        #     if deliveriesList == "" or deliveriesList == None:
        #         deliveriesList = "n/a"
        #     if driverName == "" or driverName == None:
        #         driverName = "n/a"
  
        #     queryset = DonationsForBank(deliveryBank)
        #     if queryset == False:
        #         found = 'not found'
        #         context = {'contentVal':"food bank not registered in database"}
        #         return render(request, 'drivers.html', context)
        #     elif (len(queryset) == 0):
        #         #no donations for that food bank
        #         context = {'contentVal':"no donations for that food bank - deliveries not marked"}
        #         return render(request, 'drivers.html', context)
        #     else:
        #         URL2 = "https://tranquil-tundra-49633.herokuapp.com/donation"
        #         requestedList = deliveriesList.split(', ')
        #         for k in range(len(queryset)):
        #             for j in range(len(requestedList)):
        #                 print('requestedList[j]', requestedList[j], ' queryset[k]',  queryset[k],(requestedList[j] == queryset[k]) )
        #                 if(requestedList[j] == str(queryset[k]['DonationID'])):
        #                     ToPrint = "Successful Upload for Donation ID"+str(queryset[k]['DonationID'])
        #                     newParams = queryset[k]
        #                     newParams['DonationDriver']= driverName
        #                     newParams['DonationDeliveryStatus']=True
        #                     print('newParams', newParams)
        #                     r4 = requests.put(url = URL2, json = newParams)
        #                     #returnedDonationsList= r4.json()
        #         context = {'contentVal':ToPrint}
        #         return render(request, 'drivers.html', context)
                

                            

                   
                


         



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
    context = {'contentVal': ""}
    if(request.session.get('OpenDonations') == "update successful"):
        context = {'contentVal':"update successful"}
    
    return render(request, 'drivers.html', context)
#testPutFunction()


def takeadonation(request):
    possibleDonations = request.session.get('OpenDonations')

    df = pd.DataFrame(possibleDonations)
    dfg = df.groupby(['DonationID','DonationName','DonationAllergies','DonationFoodBank','DonorEmail','DonorAddress','DonorZipCode','DonationQuantity','DonationDeliveryStatus','DonationDriver']).sum()
    ToPrint = dfg.to_html()
    ToPrint = ToPrint.replace("DonationID","ID",1)
    ToPrint = ToPrint.replace("DonationName","Food",1)
    ToPrint = ToPrint.replace("DonationAllergies","Allergies",1)
    ToPrint = ToPrint.replace("DonationFoodBank","FoodBank",1)
    ToPrint = ToPrint.replace("DonorEmail","Donor Email",1)
    ToPrint = ToPrint.replace("DonorAddress","Donor Address",1)
    ToPrint = ToPrint.replace("DonorAddress","Zip Code",1)
    ToPrint = ToPrint.replace("DonationQuantity","Quantity",1)
    ToPrint = ToPrint.replace("DonationDeliveryStatus","Delivery Status",1)
    ToPrint = ToPrint.replace("DonationDriver","Driver",1)
        
    # ToPrint = ""
    # for k in range(len(possibleDonations)):
    #     ToPrint += (json.dumps(possibleDonations[k], indent=4) + '\n')
    context = {'contentVal':ToPrint}

    if request.method == 'POST':
        driversName = request.POST.get('DriverName')
        print("Drivers Name:",driversName)
        takenDonation = request.POST.get('DonationIDTaken')
        print("taken donation:",takenDonation)

        for i in range(len(possibleDonations)):
            donationsid = possibleDonations[i]['DonationID']
            if(str(donationsid) == str(takenDonation)):
                # print("somebody pour gatorade on conrad, we gotem ======================================")
                URL = 'https://tranquil-tundra-49633.herokuapp.com/donation'
                possibleDonations[i]['DonationDeliveryStatus'] = True
                possibleDonations[i]['DonationDriver'] = driversName
                # print("this is the new dictionary:")
                # print(possibleDonations[i])
                r = requests.put(url = URL, json = possibleDonations[i])
                # context = {'contentVal':"update successful"}
                request.session['OpenDonations'] = "update successful"

                # print("lets head home boys")
                return redirect('drivers')
        
        context = {'contentVal':ToPrint+" incorrect donation id probably"}
        return render(request, 'drivers2.html', context)
    
    return render(request, 'drivers2.html', context)
