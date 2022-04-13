from django import forms
from django.forms import ModelForm
from home import models
class DonorForm(ModelForm):
    class Meta:
        model = models.FoodDonor
        fields = ('name', 'email', 'phone', 'zipcode', 'points')

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'phone':forms.TextInput(attrs={'class':'form-control'}),
            'zipcode':forms.TextInput(attrs={'class':'form-control'}),
            'points':forms.TextInput(attrs={'class':'form-control'})
        }