# Generated by Django 4.2.3 on 2023-09-04 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabler', '0004_tableb_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tablebactive',
            name='time_stop',
            field=models.DateTimeField(null=True),
        ),
    ]
