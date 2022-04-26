from rest_framework import serializers
from foodbank.models import  Donation, FoodBanks, DonationToFoodBank, banks

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Donation
        fields=('DonationID', 'DonationName', 'DonationAllergies', 'DonationFoodBank', 'DonorEmail', 'DonorAddress', 'DonorZipCode', 'DonationQuantity', 'DonationDeliveryStatus', 'DonationDriver', 'DonationExpirationDateStr')
class FoodBankSerializer(serializers.ModelSerializer):
    class Meta:
        model=FoodBanks
        fields=('FoodBankID', 'FoodBankZipCode', 'FoodBankCity', 'FoodBankName', 'FoodBankAddress')
class DonationToFoodBankSerializer(serializers.ModelSerializer):
    class Meta:
        model=DonationToFoodBank
        fields=('BridgeID', 'FoodBankIDVal', 'DonationIDVal')
class banksSerializer(serializers.ModelSerializer):
    class Meta:
        model=banks
        fields=('FoodBankID', 'FoodBankZipCode', 'FoodBankCity', 'FoodBankName', 'FoodBankAddress')

    