from django.db import models
from django.urls import reverse
from djmoney.models.fields import MoneyField

from inventory.models import Asset


# Create your models here.

class TableBType(models.Model):
    name = models.CharField(max_length=32, null=False, blank=False)
    cost = MoneyField(max_digits=16, decimal_places=0, default_currency='VND', default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tablebtype'


# "B" is shortened of "Billiards"
class TableB(models.Model):
    name = models.CharField(max_length=32, null=False, blank=False)
    type = models.ForeignKey(TableBType, on_delete=models.CASCADE, null=True)
    active = models.BooleanField(default=False)
    active_time = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tableb'


class TableBActive(models.Model):
    table_name = models.ForeignKey(TableB, on_delete=models.CASCADE, null=True)
    done = models.BooleanField(default=False)
    time_start = models.DateTimeField()
    time_stop = models.DateTimeField(null=True)
    note = models.CharField(max_length=128)

    def __str__(self):
        return self.table_name

    def get_absolute_url(self):
        return reverse("tabler:tab_act_ok", kwargs={"pk": self.pk})

    class Meta:
        db_table = 'tablebactive'


class TableBActiveOrder(models.Model):
    table_active = models.SmallIntegerField()
    order_asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    quantity_remain = models.SmallIntegerField()
    order_time = models.DateTimeField(null=True)

    def get_absolute_url(self):
        return reverse("tabler:tab_act_ok", kwargs={'pk': self.pk})

    class Meta:
        db_table = 'tablebactiveorder'


class TableBActiveOrderTmp(models.Model):
    asset_id = models.SmallIntegerField()
    asset_name = models.CharField(max_length=80)
    asset_quantity = models.SmallIntegerField()
    asset_price = MoneyField(max_digits=16, decimal_places=0, default_currency='VND', default=0)
    asset_sum = MoneyField(max_digits=16, decimal_places=0, default_currency='VND', default=0)

    class Meta:
        db_table = 'tablebactiveordertmp'


class TableBActiveSplit(models.Model):
    table_active = models.SmallIntegerField()
    split_time = models.DateTimeField()
    split_paid = MoneyField(max_digits=16, decimal_places=0, default_currency='VND', default=0)
    done = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("tabler:tab_act_ok", kwargs={'pk': self.pk})

    class Meta:
        db_table = 'tablebactivesplit'


class TableBActiveSplitOrder(models.Model):
    split_table = models.SmallIntegerField()
    order_asset = models.SmallIntegerField()
    quantity = models.SmallIntegerField()

    def get_absolute_url(self):
        return reverse("tabler:tab_act_ok", kwargs={'pk': self.pk})

    class Meta:
        db_table = 'tablebactivesplitorder'


class TableBActiveBill(models.Model):
    product = models.CharField(max_length=80, null=True)
    quantity = models.SmallIntegerField(null=True)
    price = MoneyField(max_digits=16, decimal_places=0, default_currency='VND', default=0, null=True)
    paid = MoneyField(max_digits=16, decimal_places=0, default_currency='VND', default=0, null=True)

    def get_absolute_url(self):
        return reverse("tabler:tab_act_ok", kwargs={'pk': self.pk})

    class Meta:
        db_table = 'tablebactivebill'


class TableBActiveFinish(models.Model):
    table_active = models.SmallIntegerField()
    time_start = models.DateTimeField()
    time_ended = models.DateTimeField()
    tips = MoneyField(max_digits=16, decimal_places=0, default_currency='VND', default=0, null=True)
    paid = MoneyField(max_digits=16, decimal_places=0, default_currency='VND', default=0)
    note = models.CharField(max_length=128)

    def get_absolute_url(self):
        return reverse("tabler:tab_act_ok", kwargs={'pk': self.pk})

    class Meta:
        db_table = 'tablebactivefinish'


class TableBActiveAsset(models.Model):
    timeO = models.DateTimeField(auto_now_add=True)
    userID = models.SmallIntegerField()
    treat = models.IntegerField()
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()

    def get_absolute_url(self):
        return reverse("action:treatment_asset", kwargs={'pk': self.pk})

    class Meta:
        db_table = 'tablebactiveasset'
