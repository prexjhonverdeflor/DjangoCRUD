# Generated by Django 5.0.4 on 2024-05-09 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20240509_1019'),
    ]

    operations = [
        migrations.AddField(
            model_name='bicsetup',
            name='branch',
            field=models.CharField(default='Default Branch', max_length=50),
        ),
    ]