from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm

from manager.models import Department, Employee


# from manager.models import Employee, Department, CustomerSource, Customer, Service


class RegistrationForm(UserCreationForm):
    fullname = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fullname'}))
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Valid Email is required'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    thumb = forms.ImageField(
        label='Image:', required=False,
        widget=forms.FileInput(attrs={'class': 'form-control mt-2'})
    )

    class Meta:
        model = get_user_model()
        fields = ('fullname', 'username', 'email', 'password1', 'password2', 'thumb')


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Username', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}))


class UserUpdateForm(forms.ModelForm):
    fullname = forms.CharField(
        label='Họ tên:',
        max_length=32,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'FullName'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Valid Email is required'}))
    thumb = forms.ImageField(
        label='Hình ảnh:', required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = get_user_model()
        fields = ('fullname', 'email', 'thumb')


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']


class DepartmentForm(forms.ModelForm):
    name = forms.CharField(
        label='Tên bộ phận:',
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department Name'}))

    class Meta:
        model = Department
        fields = '__all__'


class EmployeeForm(forms.ModelForm):
    humanID = \
        forms.CharField(
            label='Số CCCD/Hộ chiếu:[*]',
            strip=True,
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Citizen-ID'})
        )
    fullname = \
        forms.CharField(
            label='Họ tên:[*]',
            strip=True,
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'})
        )
    dob = \
        forms.DateField(
            label='Ngày sinh:[*]',
            widget=forms.DateInput(attrs={'type': 'date'})
        )
    mobile = \
        forms.CharField(
            label='Số điện thoại:[*]',
            strip=True,
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile Number'})
        )
    email = \
        forms.CharField(
            strip=True, required=False,
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'abc@xyz.com'})
        )
    gender = \
        forms.ChoiceField(
            label='Giới tính:[*]',
            choices=Employee.GENDER, widget=forms.Select(attrs={'class': 'form-control'})
        )
    address = \
        forms.CharField(
            label='Địa chỉ:',
            strip=True, required=False,
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'})
        )
    department = \
        forms.ModelChoiceField(
            Department.objects.all(),
            required=True,
            label='Bộ phận:[*]',
            empty_label='Chọn bộ phận',
            widget=forms.Select(attrs={'class': 'form-control'})
        )
    language = \
        forms.ChoiceField(
            label='Ngôn ngữ',
            required=False,
            choices=Employee.LANGUAGE,
            widget=forms.Select(attrs={'class': 'form-control'})
        )
    thumb = \
        forms.ImageField(
            required=False,
            label='Hình ảnh:',
            widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
        )

    class Meta:
        model = Employee
        fields = (
            'fullname', 'humanID', 'dob', 'mobile', 'email', 'address', 'salary', 'gender', 'department',
            'bank', 'nubank', 'language', 'thumb')
        widgets = {
            'salary': forms.TextInput(attrs={'class': 'form-control'}),
            'bank': forms.TextInput(attrs={'class': 'form-control'}),
            'nubank': forms.TextInput(attrs={'class': 'form-control'})
        }



