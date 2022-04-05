from unicodedata import name
from django.db import models

# Create your models here.

class Restriction(models.Model): #stuff like peanuts, dairy, gluten, halaal, kosher, etc
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class FoodDonor(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True) #can change this to twitter or reddit or whatever we decide on
    phone = models.CharField(max_length=200, null=True)
    zipcode = models.IntegerField(null=True) 
    points = models.IntegerField(null=True) 

    def __str__(self):
        return self.name


class FoodDonation(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered')
    )

    foodname = models.CharField(max_length=200, null=True)
    expirationdate = models.DateField(null=True)
    zipcode = models.IntegerField(null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    restrictions = models.ManyToManyField(Restriction)
    donor = models.ForeignKey(FoodDonor, null=True, on_delete = models.SET_NULL)


class FoodBank(models.Model):
    foodbankname = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    zipcode = models.IntegerField(null=True)
    def __str__(self):
        return self.foodbankname


class FoodBankEmployee(models.Model):
    name = models.CharField(max_length=200, null=True)
    foodbankname = models.ForeignKey(FoodBank, null=True, on_delete = models.SET_NULL) #models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True) #can change this to twitter or reddit or whatever we decide on
    phone = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class DonationRequest(models.Model):
    STATUS = (
        ('5', '5'), #very urgent
        ('4', '4'),
        ('3', '3'),
        ('2', '2'),
        ('1', '1'), 
        ('Complete', 'Complete')
    )

    description = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    zipcode = models.IntegerField(null=True)
    foodbankname = foodbankname = models.ForeignKey(FoodBank, null=True, on_delete = models.SET_NULL)

    def __str__(self):
        return self.description