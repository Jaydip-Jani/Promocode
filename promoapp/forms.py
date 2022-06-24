from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Userprofile
        fields = ['first_name', 'last_name', 'username', 'birthdate', 'gender', ]


class CouponApplyForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = "__all__"
