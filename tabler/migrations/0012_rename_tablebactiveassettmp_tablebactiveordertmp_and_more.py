# Generated by Django 4.2.3 on 2023-09-05 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tabler', '0011_tablebactiveorder_quantity'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TableBActiveAssetTmp',
            new_name='TableBActiveOrderTmp',
        ),
        migrations.AlterModelTable(
            name='tablebactiveordertmp',
            table='TableBActiveOrderTmp',
        ),
        migrations.DeleteModel(
            name='TableBActiveAsset',
        ),
    ]
