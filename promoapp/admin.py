from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Userprofile)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'birthdate', 'gender']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'start_date', 'expiration_date', 'discount_type', 'discount', 'number_of_uses',
                    'per_user_limit']


admin.site.register(Order)

# @admin.register(Order)
