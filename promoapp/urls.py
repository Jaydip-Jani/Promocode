from django.urls import path
# from . import views
# from django.views.generic import TemplateView
from .views import *

# add_order, get_code, add_code, add_coupon_order, edit_coupon, delcoupon

urlpatterns = [
    path('home/', SignUp.as_view(template_name='home.html'), name='home'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('get_user_data', add_order, name='get_user_data'),
    path('get_code/', get_code, name='get_code'),
    path('add_code/', add_code, name='add_code'),
    # get coupon or order_amount'''
    path('add_coupon_order/', add_coupon_order, name='add_coupon_order'),
    path('edit_coupon/<int:id>/', edit_coupon, name='edit_coupon'),
    path('delcoupon/<int:id>/', delcoupon, name='delcoupon'),
]
