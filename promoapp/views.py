from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import *
from .forms import *
import datetime


# Create your views here.


class SignUp(CreateView):
    model = Userprofile
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def get_code(request):
    """
    Return all code with all details.
    """

    codes = Coupon.objects.all()

    return render(
        request=request, template_name="codes.html", context={"codes": codes}
    )


def add_code(request):
    """
    Add new Code form.
    """
    context = {}
    context["form"] = CouponApplyForm()

    if request.method == "POST":

        form = CouponApplyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("get_code"))
        else:
            context["form"] = form
            return render(request, "new_code.html", context)

    return render(request, "new_code.html", context)


def add_order(request):
    if request.method == "POST":
        coupon = request.POST.get('coupon')
        order_amount = int(request.POST.get('order_amount'))

        c = Coupon.objects.filter(code=request.POST.get('coupon')).first()  # 'c' is object of Coupon model

        user = Userprofile.objects.filter(birthdate=request.user.birthdate).first()

        if not c:
            return HttpResponse("Coupon not exists.")

        # user = request.user
        if c.discount_type == "flat":

            total_amount = order_amount - c.discount
        else:
            # import pdb;
            # pdb.set_trace()
            # birthdate = datetime.datetime.strftime(user.date_of_birth, "%d-%m")
            birthdate = user.birthdate

            today_date = datetime.date.today()
            valid_date = timezone.now().date().strftime("%m-%d")

            if birthdate and birthdate.strftime("%m-%d") == valid_date:
                discount = order_amount * (c.discount / 100)
                total = order_amount - discount
                total_amount = total - (total * 0.1)
            else:
                discount = order_amount * (c.discount / 100)
                total_amount = order_amount - discount

        try:

            max_limit = c.number_of_uses
            user_limit = c.per_user_limit

            if user.is_authenticated:
                user_count = len(Order.objects.filter(user=user, coupon=c))
                coupon_count = len(Order.objects.filter(coupon=c))

                # if max_limit < user_count:
                if coupon_count > user_limit:
                    return HttpResponse("Coupon limit is over")

                if user_count > max_limit:
                    return HttpResponse("Per user limit is over")

                new_order = Order.objects.create(coupon=c, order_amount=order_amount,
                                                 total_amount=total_amount, user=request.user)
                # new_order.save()
                # c.per_user_limit = c.per_user_limit - 1
                c.number_of_uses = c.number_of_uses - 1
                c.save()
                return HttpResponseRedirect('add_coupon_order')
            else:

                return HttpResponse("Coupon limit is over")
        except Exception as e:
            return HttpResponse(e.__str__())

            # new_order = Order.objects.create(coupon=c, order_amount=order_amount,
            #                                  total_amount=total_amount, user=request.user)
            # new_order.used += 1
            # new_order.save()

            # return HttpResponseRedirect('add_coupon_order')
    #     else:
    return render(request, "user_data.html")


def add_coupon_order(request):
    # coupon, order_amount):
    """
    add coupon info into order model
    """
    codes = Order.objects.all()

    return render(request, 'orders.html', {'codes': codes})


def edit_coupon(request, id):
    coupon = Coupon.objects.get(id=id)
    # order_count = coupon.coupon_related.filter().count()
    form = CouponApplyForm(request.POST, instance=coupon)
    if form.is_valid():
        form.save()
        return redirect('/get_code/')
    else:
        form = CouponApplyForm(instance=coupon)
    context = {'codes': form}
    return render(request, 'edit.html', context)


def delcoupon(request, id):
    coupon = Coupon.objects.get(pk=id)
    order_count = coupon.coupon_related.filter().count()

    if order_count:
        return HttpResponse("You can not delete used coupon")
    else:
        coupon.delete()
        return redirect('get_code')
