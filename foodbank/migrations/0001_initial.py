# Generated by Django 4.0.3 on 2022-04-11 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='banks',
            fields=[
                ('FoodBankID', models.AutoField(primary_key=True, serialize=False)),
                ('FoodBankZipCode', models.CharField(max_length=500)),
                ('FoodBankCity', models.CharField(max_length=500)),
                ('FoodBankName', models.CharField(max_length=500)),
                ('FoodBankAddress', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('DonationID', models.AutoField(primary_key=True, serialize=False)),
                ('DonationName', models.CharField(max_length=500)),
                ('DonationAllergies', models.CharField(max_length=500)),
                ('DonationFoodBank', models.CharField(max_length=500)),
                ('DonorEmail', models.CharField(max_length=500)),
                ('DonorAddress', models.CharField(max_length=500)),
                ('DonorZipCode', models.CharField(max_length=500)),
                ('DonationQuantity', models.IntegerField()),
                ('DonationDeliveryStatus', models.BooleanField(null=False)),
                ('DonationDriver', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='DonationToFoodBank',
            fields=[
                ('BridgeID', models.AutoField(primary_key=True, serialize=False)),
                ('FoodBankIDVal', models.CharField(max_length=500)),
                ('DonationIDVal', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='FoodBanks',
            fields=[
                ('FoodBankID', models.AutoField(primary_key=True, serialize=False)),
                ('FoodBankZipCode', models.CharField(max_length=500)),
                ('FoodBankCity', models.CharField(max_length=500)),
                ('FoodBankName', models.CharField(max_length=500)),
                ('FoodBankAddress', models.CharField(max_length=500)),
            ],
        ),
    ]
