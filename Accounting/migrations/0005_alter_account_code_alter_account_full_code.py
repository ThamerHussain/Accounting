# Generated by Django 4.0.6 on 2022-08-03 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounting', '0004_alter_account_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='full_code',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
