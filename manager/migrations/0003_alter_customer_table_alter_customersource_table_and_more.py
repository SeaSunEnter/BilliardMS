# Generated by Django 4.2.3 on 2023-09-16 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_delete_birthday'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='customer',
            table='customer',
        ),
        migrations.AlterModelTable(
            name='customersource',
            table='customersource',
        ),
        migrations.AlterModelTable(
            name='department',
            table='department',
        ),
        migrations.AlterModelTable(
            name='employee',
            table='employee',
        ),
        migrations.AlterModelTable(
            name='loginlogs',
            table='loginlogs',
        ),
        migrations.AlterModelTable(
            name='service',
            table='service',
        ),
        migrations.AlterModelTable(
            name='user',
            table='user',
        ),
    ]