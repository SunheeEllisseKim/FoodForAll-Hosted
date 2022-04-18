from django.db import models

# Create your models here.

# model to store department and employee details
class Donation(models.Model):
    DonationID = models.AutoField(primary_key=True)
    DonationName = models.CharField(max_length=500, blank=True)
    DonationAllergies = models.CharField(max_length=500, blank=True)
    DonationFoodBank= models.CharField(max_length=500, blank=True)
    DonorEmail = models.CharField(max_length=500, blank=True)
    DonorAddress = models.CharField(max_length=500, blank=True)
    DonorZipCode = models.CharField(max_length=500, blank=True)
    DonationQuantity =models.IntegerField()
    DonorTwitter = models.CharField(max_length=500)

class FoodBanks(models.Model):
    FoodBankID = models.AutoField(primary_key=True)
    FoodBankZipCode = models.CharField(max_length=500)
    FoodBankCity = models.CharField(max_length=500)
    FoodBankName = models.CharField(max_length=500)
    FoodBankAddress = models.CharField(max_length=500)
class banks(models.Model):
    FoodBankID = models.AutoField(primary_key=True)
    FoodBankZipCode = models.CharField(max_length=500)
    FoodBankCity = models.CharField(max_length=500)
    FoodBankName = models.CharField(max_length=500)
    FoodBankAddress = models.CharField(max_length=500)
class DonationToFoodBank(models.Model):
    BridgeID = models.AutoField(primary_key=True)
    FoodBankIDVal = models.CharField(max_length=500)
    DonationIDVal = models.CharField(max_length=500)
   