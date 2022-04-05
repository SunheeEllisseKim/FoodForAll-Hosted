from django.contrib import admin

from .models import *
admin.site.register(Restriction)
admin.site.register(FoodDonor)
admin.site.register(FoodDonation)
admin.site.register(FoodBank)
admin.site.register(FoodBankEmployee)
admin.site.register(DonationRequest)

# Register your models here.
