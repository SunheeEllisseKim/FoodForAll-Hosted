from django.shortcuts import render
# from requests import post
import requests
from foodbank.models import Donation, FoodBanks, banks
import json

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
                if (donationFoodBank == str(foodbankID)):
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


def drivers(request):
    if request.method == 'POST':
        userinput = request.POST.get('FoodBankName')
        print("USER INPUT: ", userinput)
        queryset = DonationsForBank(userinput)
        if queryset == False:
            #couldn't find food bank
            context = {'string':"food bank not registered in database"}
            return render(request, 'drivers.html', context)
        elif (len(queryset) == 0):
            #no donations for that food bank
            context = {'string':"no donations for that food bank"}
            return render(request, 'drivers.html', context)
        else:
            pretty = json.dumps(queryset[0], indent=4)
            print("=========="*13)
            # print(type(pretty))
            ToPrint = ""
            for k in range(len(queryset)):
                ToPrint += (json.dumps(queryset[k], indent=4) + '\n\n')
            context = {'string':ToPrint}
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

