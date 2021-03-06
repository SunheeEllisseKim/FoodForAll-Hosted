from django.db import models

# Create your models here.

# model to store department and employee details
class Donation(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered')
    )
    DonationID = models.AutoField(primary_key=True)
    DonationName = models.CharField(max_length=500)
    DonationAllergies = models.CharField(max_length=500)
    DonationFoodBank= models.CharField(max_length=500)
    DonorEmail = models.CharField(max_length=500)
    DonorAddress = models.CharField(max_length=500)
    DonorZipCode = models.CharField(max_length=500)
    DonationQuantity =models.IntegerField()
    DonationDeliveryStatus = models.BooleanField(null=False)
    DonationDriver= models.CharField(max_length=500)
    DonationExpirationDateStr = models.CharField(max_length=500)
   
    Status = models.CharField(max_length=200, null=True, choices=STATUS)

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
   