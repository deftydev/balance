# Generated by Django 2.2.14 on 2020-07-28 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200728_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='balance',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='contact',
            field=models.IntegerField(null=True),
        ),
    ]
