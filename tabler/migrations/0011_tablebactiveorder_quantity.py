# Generated by Django 4.2.3 on 2023-09-05 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabler', '0010_alter_tablebactiveorder_order_asset_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tablebactiveorder',
            name='quantity',
            field=models.SmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]