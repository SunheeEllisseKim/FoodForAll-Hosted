from django import forms
from django.forms import ModelForm
from foodbank import models

class DonorForm(ModelForm):
    class Meta:
        model = models.Donation
        fields = ('DonorTwitter', 'DonorEmail','DonorAddress', 'DonorZipCode', 'DonationName', 'DonationQuantity', 'DonationAllergies', 'DonationFoodBank')
        labels = {
            'DonorTwitter': 'Twitter Handle',
            'DonorEmail':'Email',
            'DonorAddress':'Address',
            'DonorZipCode':'Zip Code',
            'DonationName': 'Food',
            'DonationQuantity': 'Qty',
            'DonationAllergies': 'Allergy Concerns',
            'DonationFoodBank': 'Food Bank',
        }
        widgets = {
            'DonorTwitter':forms.TextInput(attrs={'class':'form-control', 'name':"content"}),
            'DonorEmail':forms.EmailInput(attrs={'class':'form-control'}),
            'DonorAddress':forms.TextInput(attrs={'class':'form-control'}),
            'DonorZipCode':forms.TextInput(attrs={'class':'form-control'}),
            'DonationName': forms.TextInput(attrs={'class':'form-control'}),
            'DonationQuantity': forms.TextInput(attrs={'class':'form-control'}),
            'DonationAllergies': forms.TextInput(attrs={'class':'form-control'}),
            'DonationFoodBank': forms.TextInput(attrs={'class':'form-control'}),
        }