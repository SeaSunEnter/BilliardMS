# Generated by Django 4.2.3 on 2023-09-16 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_asset_unitinout'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='assetcategory',
            table='assetcategory',
        ),
        migrations.AlterModelTable(
            name='assetunit',
            table='assetunit',
        ),
        migrations.AlterModelTable(
            name='inventory',
            table='inventory',
        ),
        migrations.AlterModelTable(
            name='inventorytmp',
            table='inventorytmp',
        ),
        migrations.AlterModelTable(
            name='purchase',
            table='purchase',
        ),
        migrations.AlterModelTable(
            name='supplier',
            table='supplier',
        ),
    ]
