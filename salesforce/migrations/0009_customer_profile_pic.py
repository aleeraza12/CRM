# Generated by Django 3.0.4 on 2020-04-06 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salesforce', '0008_customer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
