from django.db import models

from datetime import date
from django.contrib.auth.models import AbstractUser, User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone
from django.conf import settings



# from testapp.core.models import User


GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'),)
DISCOUNT_CHOICES = (("percentage", "Percentage"), ("flat", "Flat"))


class Userprofile(AbstractUser):
    # user_name = models.CharField(max_length=30)
    # firs_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthdate = models.DateField(blank=False, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return "{}".format(self.username)

#
# class Userprofile(AbstractUser):
#     date_of_birth = models.DateField(blank=False, null=True)
#     gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
#
#     def __str__(self):
#         return "{}".format(self.username)


class Coupon(models.Model):
    def validate_date(value):
        v = timezone.now()
        if value < v:
            raise ValidationError("please don't enter a pastdate")

    def validate_start(start):

        d = timezone.now()
        if start < d:
            raise ValidationError("enter valid date ")

    code = models.CharField(max_length=6, unique=True,  # help_text="Only uppercase letters & numbers are allowed.",
                            validators=[
                                RegexValidator("^[A-Z0-9]*$", "Only uppercase letters & numbers are allowed.", )], )
    start_date = models.DateTimeField(validators=[validate_start], null=True, blank=True)
    expiration_date = models.DateTimeField(validators=[validate_date], null=True, blank=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_CHOICES)
    discount = models.PositiveIntegerField()
    number_of_uses = models.PositiveIntegerField(
        # help_text="How many times this coupon will be used.", default=1
    )
    per_user_limit = models.PositiveIntegerField()


class Order(models.Model):
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='user_related')
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='coupon_related')
    order_amount = models.IntegerField(validators=[MinValueValidator(100), MaxValueValidator(150000)])
    total_amount = models.PositiveIntegerField(
        # help_text="Order total amount after code redemption applied."
    )

    def __str__(self):
        return "{} - {}".format(self.user.username, self.coupon.code)

    @property
    def discount_amout(self):
        """
        return coupon gender
        """

        return self.order_amount - self.total_amount
