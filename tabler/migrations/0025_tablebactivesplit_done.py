# Generated by Django 4.2.3 on 2023-09-11 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabler', '0024_tablebactiveorder_quantity_remain'),
    ]

    operations = [
        migrations.AddField(
            model_name='tablebactivesplit',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]
