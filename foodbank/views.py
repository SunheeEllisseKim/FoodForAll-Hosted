from django.shortcuts import render
from django.http import HttpResponse
import datetime


from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from foodbank.models import FoodBanks, Donation, DonationToFoodBank, banks
from foodbank.serializers import FoodBankSerializer,DonationSerializer, DonationToFoodBankSerializer, banksSerializer



@csrf_exempt
def bankApi(request, id=0):
    if request.method=='GET':
        bank = banks.objects.all()
        bank_serializer=banksSerializer(bank,many=True)
        return JsonResponse(bank_serializer.data,safe=False)
    elif request.method=='POST':
        bank_data=JSONParser().parse(request)
        bank_serializer = banksSerializer(data=bank_data)
        if bank_serializer.is_valid():
            bank_serializer.save()
            return JsonResponse("Successfully added", safe=False)
        return JsonResponse("Failure to add", safe=False)
    elif request.method=='PUT':
        bank_data=JSONParser().parse(request)
        bank = banks.objects.get(FoodBankID=bank_data['FoodBankID'])
        bank_serializer=banksSerializer(bank,data=bank_data)

        if bank_serializer.is_valid():
            bank_serializer.save()
            return JsonResponse("Successfully updated", safe=False)
        return JsonResponse("Failure to update", safe=False)
    elif request.method=='DELETE':
        bank = banks.objects.get(FoodBankID=id)
        bank.delete()

        return JsonResponse("Deletion successful", safe=False)
@csrf_exempt
def foodBankApi(request, id=0):
    if request.method=='GET':
        foodbank = FoodBanks.objects.all()
        foodbank_serializer=FoodBankSerializer(foodbank,many=True)
        return JsonResponse(foodbank_serializer.data,safe=False)
    elif request.method=='POST':
        foodbank_data=JSONParser().parse(request)
        foodbank_serializer = FoodBankSerializer(data=foodbank_data)
        if foodbank_serializer.is_valid():
            foodbank_serializer.save()
            return JsonResponse("Successfully added", safe=False)
        return JsonResponse("Failure to add", safe=False)
    elif request.method=='PUT':
        '''
        bank_data=JSONParser().parse(request)
        bank = banks.objects.get(FoodBankID=bank_data['FoodBankID'])
        bank_serializer=banksSerializer(bank,data=bank_data)

        if bank_serializer.is_valid():
            bank_serializer.save()
            return JsonResponse("Successfully updated", safe=False)
        return JsonResponse("Failure to update", safe=False)
        '''
        foodbank_data=JSONParser().parse(request)
        foodbank = FoodBanks.objects.get(FoodBankID=foodbank_data['FoodBankID'])
        foodbank_serializer=FoodBankSerializer(foodbank,data=foodbank_data)

        if foodbank_serializer.is_valid():
            foodbank_serializer.save()
            return JsonResponse("Successfully updated", safe=False)
        return JsonResponse("Failure to update", safe=False)
    elif request.method=='DELETE':
        foodbank = FoodBanks.objects.get(FoodBankID=id)
        foodbank.delete()

        return JsonResponse("Deletion successful", safe=False)

@csrf_exempt
def donationToFoodBankApi(request, id=0):
    if request.method=='GET':
        donationToFoodBank = DonationToFoodBank.objects.all()
        donationToFoodBank_serializer=DonationToFoodBankSerializer(donationToFoodBank,many=True)
        return JsonResponse(donationToFoodBank_serializer.data,safe=False)
    elif request.method=='POST':
        donationToFoodBank_data=JSONParser().parse(request)
        donationToFoodBank_serializer = DonationToFoodBankSerializer(data=donationToFoodBank_data)
        if donationToFoodBank_serializer.is_valid():
            donationToFoodBank_serializer.save()
            return JsonResponse("Successfully added", safe=False)
        return JsonResponse("Failure to add", safe=False)
    elif request.method=='PUT':
        '''
        bank_data=JSONParser().parse(request)
        bank = banks.objects.get(FoodBankID=bank_data['FoodBankID'])
        bank_serializer=banksSerializer(bank,data=bank_data)

        if bank_serializer.is_valid():
            bank_serializer.save()
            return JsonResponse("Successfully updated", safe=False)
        return JsonResponse("Failure to update", safe=False)
        '''

        donationToFoodBank_data=JSONParser().parse(request)
        donationToFoodBank = DonationToFoodBank.objects.get(BridgeID=donationToFoodBank_data['BridgeID'])
        donationToFoodBank_serializer=DonationToFoodBankSerializer(donationToFoodBank,data=donationToFoodBank_data)

        if donationToFoodBank_serializer.is_valid():
            donationToFoodBank_serializer.save()
            return JsonResponse("Successfully updated", safe=False)
        return JsonResponse("Failure to update", safe=False)
    elif request.method=='DELETE':
        donationToFoodBank = FoodBanks.objects.get(BridgeID=id)
        donationToFoodBank.delete()

        return JsonResponse("Deletion successful", safe=False)
@csrf_exempt
def donationApi(request, id=0):
    if request.method=='GET':
        donation = Donation.objects.all()
        donation_serializer=DonationSerializer(donation,many=True)
        return JsonResponse(donation_serializer.data,safe=False)
    elif request.method=='POST':
        donation_data=JSONParser().parse(request)
        donation_serializer = DonationSerializer(data=donation_data)
        if donation_serializer.is_valid():
            donation_serializer.save()
            return JsonResponse("Successfully added", safe=False)
        return JsonResponse("Failure to add", safe=False)
    elif request.method=='PUT':
        '''
        bank_data=JSONParser().parse(request)
        bank = banks.objects.get(FoodBankID=bank_data['FoodBankID'])
        bank_serializer=banksSerializer(bank,data=bank_data)

        if bank_serializer.is_valid():
            bank_serializer.save()
            return JsonResponse("Successfully updated", safe=False)
        return JsonResponse("Failure to update", safe=False)
        '''
        donation_data=JSONParser().parse(request)
        donation = Donation.objects.get(DonationID=donation_data['DonationID'])
        donation_serializer=DonationSerializer(donation,data=donation_data)

        if donation_serializer.is_valid():
            donation_serializer.save()
            return JsonResponse("Successfully updated", safe=False)
        return JsonResponse("Failure to update", safe=False)
    elif request.method=='DELETE':
        donation = FoodBanks.objects.get(DonationID=id)
        donation.delete()

        return JsonResponse("Deletion successful", safe=False)

print("VIEWS>.py")
TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates)'
)
from foodbank import foodBankAndCovid 


# Create your views here.
def index(request):
    print('reach INDEX')
    print("at INDEX", request)
    today = datetime.datetime.now().date()
    print("***")
    #foodBankAndCovidData = foodBankAndCovid()
    foodBankAndCovidData = foodBankAndCovid.returnDataForRecipient('115 New Cavendish Street')
    #print("here getFoodBankAndCovidData",foodBankAndCovidData)

    #response = HttpResponse('index.html')
    # print('response', response)
    #response.write("<p>Here's the text of the web page.</p>")
    #response.write("<p>Here's another paragraph.</p>")

    #foodBankAndCovidData = "\n\n <span style="white-space: pre-line"> <br> <<br/>> <p>This is Line1 </span></p> <p>This is Line2</p>here we go"
    #v = render(request, "index.html", {"today": today})
    val = foodBankAndCovid.returnDatabaseFoodBanks()
    if request.method == 'POST':
            print("POST METHOD")
            content = request.POST.get('content', '')
            print("inputAddress")
            content2 = request.POST.get('content2', '')
            if content2:
                print('Content2', content2)
            if content:
                print('Content', content)
                foodBankAndCovidData = foodBankAndCovid.returnDataForRecipient(str(content))
    if request.method == 'POST1':
            print("POST1 METHOD")
            content = request.POST1.get('content', '')
            print("inputAddress")
            if content:
                print('Content', content)
                foodBankAndCovidData = foodBankAndCovid.returnDataForRecipient(str(content))   

    #inputAddress = request.POST.get('inputAddress', '')
    #render(request, "index1.html", {"test": "testingrenderrequewst"})
    return render(request, "index1.html", {"FoodBankData": foodBankAndCovidData})
def index2(request):
    print("INDEX 2 foodbank")
    print("at INDEX", request)
    today = datetime.datetime.now().date()
    print("***")
    #foodBankAndCovidData = foodBankAndCovid()
    foodBankAndCovidData = foodBankAndCovid.returnDataForRecipient('115 New Cavendish Street')
    #print("here getFoodBankAndCovidData",foodBankAndCovidData)

    #response = HttpResponse('index.html')
    # print('response', response)
    #response.write("<p>Here's the text of the web page.</p>")
    #response.write("<p>Here's another paragraph.</p>")

    #foodBankAndCovidData = "\n\n <span style="white-space: pre-line"> <br> <<br/>> <p>This is Line1 </span></p> <p>This is Line2</p>here we go"
    #v = render(request, "index.html", {"today": today})
    val = foodBankAndCovid.returnDatabaseFoodBanks()

    #return inputAddress = request.POST.get('inputAddress', '')
    return render(request, "index1.html", {"test": "testingrenderrequewst"})