from django import forms

from inventory.models import Asset
from tabler.models import TableBType, TableB, TableBActive, TableBActiveOrder, TableBActiveSplit, TableBActiveFinish


class TableBTypeForm(forms.ModelForm):
    name = forms.CharField(
        max_length=64,
        label='Loại bàn',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Loại bàn'})
    )

    class Meta:
        model = TableBType
        fields = ('id', 'name', 'cost')
        labels = {'cost': 'Giá tiền (/phút):'}


class TableBForm(forms.ModelForm):
    name = \
        forms.CharField(
            label='Tên bàn:',
            strip=True,
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Table Name'})
        )
    type = \
        forms.ModelChoiceField(
            TableBType.objects.all(),
            required=True,
            label='Loại bàn',
            empty_label='Chọn Loại bàn',
            widget=forms.Select(attrs={'class': 'form-control'})
        )

    class Meta:
        model = TableB
        fields = ('id', 'name', 'type')


class TableBActiveForm(forms.ModelForm):
    time_input = \
        forms.TimeField(
            required=False,
            label='Bắt đầu:',
            widget=forms.TimeInput(attrs={'type': 'time'}, format='%H:%M')
            # widget=DatePickerInput()
        )
    note = \
        forms.CharField(
            label='Ghi chú:',
            required=False,
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'})
        )

    class Meta:
        model = TableBActive
        fields = ('note',)


class TableBActiveFilterForm(forms.Form):
    mobile: forms.CharField()


class TableBActiveOrderForm(forms.ModelForm):
    order_asset = forms.ModelChoiceField(
        # Asset.objects.filter(inventory__idIO__gt=0).distinct(),
        # Asset.objects.filter(inventory__quantityIO__gt=0).order_by('name').distinct(),
        Asset.objects.all(),
        label='Sản phẩm:',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    quantity = forms.IntegerField(
        label='Số lượng:',
        widget=forms.NumberInput()
    )

    class Meta:
        model = TableBActiveOrder
        fields = ('order_asset', 'quantity')


class TableBActiveAskFinishForm(forms.ModelForm):
    time_input = \
        forms.TimeField(
            required=False,
            label='Kết thúc:',
            widget=forms.TimeInput(attrs={'type': 'time'}, format='%H:%M')
            # widget=DatePickerInput()
        )
    note = \
        forms.CharField(
            label='Ghi chú:',
            required=False,
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'})
        )

    class Meta:
        model = TableBActiveFinish
        fields = ('note',)


class TableBActiveFinishForm(forms.ModelForm):
    quantity = forms.IntegerField(
        label='Số lượng:',
        widget=forms.NumberInput()
    )

    class Meta:
        model = TableBActiveFinish
        fields = ('time_start', 'time_ended')


class TableBActiveSplitForm(forms.ModelForm):
    time_input = \
        forms.TimeField(
            required=False,
            label='Ngắt cơ lúc:',
            widget=forms.TimeInput(attrs={'type': 'time'}, format='%H:%M')
            # widget=DatePickerInput()
        )

    class Meta:
        model = TableBActiveSplit
        fields = ()
