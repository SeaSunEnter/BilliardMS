# Generated by Django 4.2.3 on 2023-09-02 15:46

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_inventorytmp'),
        ('tabler', '0002_alter_tableb_name_tablebactive'),
    ]

    operations = [
        migrations.CreateModel(
            name='TableBActiveAssetTmp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_id', models.SmallIntegerField()),
                ('asset_name', models.CharField(max_length=80)),
                ('asset_quantity', models.SmallIntegerField()),
                ('asset_price_currency', djmoney.models.fields.CurrencyField(choices=[('USD', 'USD $'), ('VND', 'VN ₫')], default='VND', editable=False, max_length=3)),
                ('asset_price', djmoney.models.fields.MoneyField(decimal_places=0, default=Decimal('0'), default_currency='VND', max_digits=16)),
                ('asset_sum_currency', djmoney.models.fields.CurrencyField(choices=[('USD', 'USD $'), ('VND', 'VN ₫')], default='VND', editable=False, max_length=3)),
                ('asset_sum', djmoney.models.fields.MoneyField(decimal_places=0, default=Decimal('0'), default_currency='VND', max_digits=16)),
            ],
            options={
                'db_table': 'TableBActiveAssetTmp',
            },
        ),
        migrations.CreateModel(
            name='TableBActiveProcess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.IntegerField()),
                ('date', models.DateField(max_length=10)),
                ('status', models.TextField(max_length=128)),
                ('tmp_thumb', models.ImageField(blank=True, null=True, upload_to='TableBActives')),
            ],
            options={
                'db_table': 'TableBActiveProcess',
            },
        ),
        migrations.AddField(
            model_name='tablebactive',
            name='done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tablebactive',
            name='note',
            field=models.CharField(default=0, max_length=128),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='TableBActiveAsset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeO', models.DateTimeField(auto_now_add=True)),
                ('userID', models.SmallIntegerField()),
                ('treat', models.IntegerField()),
                ('quantity', models.SmallIntegerField()),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.asset')),
            ],
            options={
                'db_table': 'TableBActiveAsset',
            },
        ),
    ]