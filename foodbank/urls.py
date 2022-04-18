from django.urls import include, re_path
from foodbank import views
from django.urls import path
from . import views

''' Postman

Postman DELETE http://127.0.0.1:8000/banks/2 (delete FoodBankID=2)

banks:
{
    
    "FoodBankZipCode": "WC2H 9LA",
    "FoodBankCity": "London",
    "FoodBankName": "Covent Garden",
    "FoodBankAddress": "42 Earlham Street"

}

donations:
{
    
    "DonationName": "Canned Soup",
    "DonationAllergies": "n/a",
    "DonationFoodBank": "2",
    "DonationQuantity": 9



}


'''
print("foodbank urls py")

urlpatterns=[
    path('',views.index, name='index'),
    re_path(r'^foodbanks$',views.foodBankApi),
    re_path(r'^foodbanks/([0-9]+)$', views.foodBankApi),

    re_path(r'^donationToFoodBank$',views.donationToFoodBankApi),
    re_path(r'^donationToFoodBank/([0-9]+)$', views.donationToFoodBankApi),

    re_path(r'^donation$',views.donationApi),
    re_path(r'^donation/([0-9]+)$', views.donationApi),

    
    re_path(r'^banks$',views.bankApi),
    re_path(r'^banks/([0-9]+)$', views.bankApi),

  
]