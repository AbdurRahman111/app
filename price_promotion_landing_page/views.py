from django.shortcuts import render, redirect
from .models import any_product_discount, Category_level_discount, Specific_Level_Product_Deals, subscribe_app_3
# Create your views here.


def landing_page_three(request):
    all_any = any_product_discount.objects.all()
    all_cate = Category_level_discount.objects.all()
    all_specific = Specific_Level_Product_Deals.objects.all()

    context = {'all_any': all_any, 'all_cate': all_cate, 'all_specific': all_specific}

    return render(request, 'price_promotion_landing_page.html', context)


def subscribes_app3(request):
    subscribe_email = request.POST.get('subscribe_email')

    data_subscribe = subscribe_app_3(email=subscribe_email)
    data_subscribe.save()
    return redirect('landing_page_three')