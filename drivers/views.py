from django.shortcuts import render
from requests import post
from foodbank.models import Donation, FoodBanks, banks

# Create your views here.

def DonationsForBank(userinput):
    foodbank = banks.object.get(FoodBankName=userinput)
    print("FOODBANK:", foodbank)
    foodbankid = foodbank.FoodBankID

    queryset = Donation.objects.filter(DonationFoodBank=foodbankid)

    return queryset


def drivers(request):
    if request.method == 'POST':
        userinput = request.POST.get('FoodBankName')
        print("USER INPUT: ", userinput)
        queryset = DonationsForBank(userinput)
        if queryset:
            string = ""
            for i in queryset:
                string += (str(i)+'\n')
            context = {'string':string}

            return render(request, 'drivers.html', context)
        else:
            context = {'string':"no donations found"}
            return render(request, 'drivers.html', context)
    else:
        context = {'string':"string"}
        return render(request, 'drivers.html', context)

