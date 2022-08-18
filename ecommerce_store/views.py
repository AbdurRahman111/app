from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .models import EmailConfirmed, products, Order, Categories, contact_us, reviews, subscribe, loyalty_registration_table, loyalty_benefit_info_table, coupon_rate, any_product_discount, Category_level_discount, Specific_Level_Product_Deals, Contact_Info, About_Us_Info, Our_Blog, Home_Banner, Stripe_Api
from django.shortcuts import get_object_or_404
import random
from django.db.models import Q
import stripe
from django.conf import settings
from django.urls import reverse
from django.views.generic import ListView, DetailView, View
# Create your views here.
import uuid

from django.views.decorators.csrf import csrf_exempt
import stripe
from django.core import serializers
from django.http import JsonResponse



def landing_page_two(request):
    all_products = products.objects.all()
    all_Categories = Categories.objects.all()
    all_banner = Home_Banner.objects.all()
    context1 = {'all_products': all_products, 'all_Categories': all_Categories, 'all_banner':all_banner}
    return render(request, 'index.html', context1)





def product_search(request):
    search_product  = request.GET.get('search')
    print(search_product)

    if search_product:
        search_result = products.objects.filter(Q(product_name__icontains = search_product) | Q(description__icontains = search_product)).order_by('-id')

        search_result_count = products.objects.filter(Q(product_name__icontains = search_product) | Q(description__icontains = search_product)).count()


        context5 = {'search_product':search_product, 'search_result' :search_result, 'search_result_count':search_result_count}
        return render(request, 'product.html', context5)



def blog(request):
    all_blogs = Our_Blog.objects.all()
    context = {'all_blogs':all_blogs}
    return render(request, 'blog.html', context)


def about(request):
    all_inf = About_Us_Info.objects.all()
    context = {'all_inf':all_inf}
    return render(request, 'about.html', context)


def contact(request):
    if request.method=="POST":
        email=request.POST.get('email')
        msg=request.POST.get('msg')
        print(email, msg)

        contactus = contact_us(email=email, message=msg)
        contactus.save()
        messages.success(request, 'Message Has been sent to admin !!')
        return redirect('landing_page_two')

    all_infos = Contact_Info.objects.last()
    return render(request, 'contact.html', {'all_infos':all_infos})

def profile(request):
    return render(request, 'profile.html')

def subscribe_users(request):
    subscribe_email = request.POST.get('subscribe_email')

    data_subscribe=subscribe(email=subscribe_email)
    data_subscribe.save()
    return redirect('landing_page_two')

def my_orders(request):
    user = request.user
    get_all_order = Order.objects.filter(user=user)
    context = {'get_all_order':get_all_order}
    return render(request, 'my_order.html', context)

def signup_login(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email_sign = request.POST.get('email_sign')
        password_sign = request.POST.get('password_sign')
        password_sign_re = request.POST.get('password_sign_re')


        # chech the error inputs
        user_email_info = User.objects.filter(email=email_sign)

        erorr_message = ""

        if user_email_info:
            # messages.error(request, "Email Already Exist")
            erorr_message = "Email Already Exist"

        elif password_sign != password_sign_re:
            # messages.error(request, "Passwords are not match")
            erorr_message = "Passwords are not match !!"

        elif len(password_sign) < 7:
            # messages.error(request, "Passwords Must be Al least 7 Digits")
            erorr_message = "Passwords Must be Al least 7 Digits !!"

        if not erorr_message:

            # create user
            myuser = User.objects.create_user(email_sign, email_sign, password_sign)
            myuser.first_name = first_name
            myuser.last_name = last_name
            myuser.is_active = False
            myuser.save()

            # send mail
            user = EmailConfirmed.objects.get(user=myuser)
            site = get_current_site(request)
            email = myuser.email
            first_name = myuser.first_name
            last_name = myuser.last_name

            sub_of_email = "Activation Email From Medicify."
            email_body = render_to_string(
                'verify_email.html',
                {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'domain': site.domain,
                    'activation_key': user.activation_key
                }
            )

            send_mail(
                sub_of_email,  # Subject of message
                email_body,  # Message
                '',  # From Email
                [email],  # To Email

                fail_silently=True
            )

            messages.success(request, 'Check Your Email for Activate Your Account !!!')

            return redirect('/')

        else:

            value_dic = {'first_name': first_name, 'last_name': last_name, 'email_sign': email_sign,
                         'erorr_message': erorr_message}
            return render(request, 'signup_func.html', value_dic)
    return render(request, 'signup_func.html')



def email_confirm(request, activation_key):
    user= get_object_or_404(EmailConfirmed, activation_key=activation_key)
    if user is not None:
        user.email_confirmed=True
        user.save()

        myuser=User.objects.get(email=user)
        myuser.is_active=True
        myuser.save()
        first_name=myuser.first_name
        last_name=myuser.last_name

        condict = {'first_name': first_name, 'last_name':last_name}
        return render(request, 'registration_complete.html', condict)


def login_func(request):
    if request.method == 'POST':
        log_username = request.POST['log_username']
        log_password = request.POST['log_password']
        # this is for authenticate username and password for login
        user = authenticate(username=log_username, password=log_password)

        erorr_message_2 = ""

        if user is not None:
            login(request, user)
            # messages.success(request, "Successfully Logged In !!")
            return redirect('landing_page_two')
        else:
            erorr_message_2 ="Invalid Credentials, Please Try Again !!"

            value_func2 = {'erorr_message_2':erorr_message_2, 'log_username':log_username}
            # messages.error(request, "Invalid Credentials, Please Try Again !!")
            return render(request, 'signup_func.html', value_func2)


def logout_func(request):
    # this is for logout from user id
    logout(request)
    return redirect('landing_page_two')


def product_detail(request, pk):
    get_product = products.objects.get(id=pk)
    # products category
    cat_pro = get_product.category
    # get all product by category
    all_pro_cat = products.objects.filter(category=cat_pro)

    filter_product_reviews = reviews.objects.filter(product=get_product).order_by('-id')
    filter_product_reviews_qty = reviews.objects.filter(product=get_product).count()

    # making average rating
    total_ratings=0
    for i in filter_product_reviews:
        total_ratings = total_ratings + int(i.ratings)
        print(total_ratings)

    if filter_product_reviews_qty==0:
        average_rating = 0
    else:
        average_rating = total_ratings/filter_product_reviews_qty
        print(average_rating)

    average_rating = "%0.1f" % average_rating


    context2 = {'get_product':get_product, 'all_pro_cat':all_pro_cat, 'filter_product_reviews':filter_product_reviews, 'filter_product_reviews_qty':filter_product_reviews_qty, 'average_rating':average_rating}
    return render(request, 'product-detail.html', context2)

def customer_review(request):
    rating_number=request.POST.get('rating_number')
    review_text=request.POST.get('review_text')

    product_id=request.POST.get('product_id')
    get_details_product = products.objects.get(id=product_id)

    user = request.user

    filter_review = reviews.objects.filter(customer=user, product=get_details_product)

    if filter_review:
        messages.success(request, 'You Can not Give Feedback More Than Once.')
        return redirect('product_detail', product_id)
    else:

        data_reviews = reviews(customer=user, product=get_details_product, ratings=rating_number, review_text=review_text)
        data_reviews.save()

        messages.success(request, 'Your Review Has Been Added !!')
        return redirect('product_detail', product_id)


def cart(request):
    # stripe.api_key = settings.STRIPE_PRIVET_KEY
    #
    # session = stripe.checkout.Session.create(
    #     payment_method_types=['card'],
    #     line_items=[{
    #         'price': 'price_1IWudUFzvY3Oon8K1C66bAva',
    #         'quantity': 1,
    #     }],
    #     mode='payment',
    #     success_url=request.build_absolute_uri(reverse('checkout')) + '?session_id={CHECKOUT_SESSION_ID}',
    #     cancel_url=request.build_absolute_uri(reverse('cart')),
    # )
    return render(request, 'shoping-cart.html')#, {'session_id':session.id, 'stripe_public_key':settings.STRIPE_PUBLIC_KEY})


def checkout(request):
    if request.method =="POST":
        prod_details = request.POST.get('prod_details')
        checkout_money = request.POST.get('checkout_money')
        total_money_last = request.POST.get('total_money_last')

        print('total_money_last')
        print(total_money_last)

        print('total')
        print(checkout_money, prod_details)

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        country = request.POST.get('country')
        street = request.POST.get('street')
        city = request.POST.get('city')
        zip = request.POST.get('zip')
        # print(full_address, city, postal_code, country, phone)

        # make random order ID
        random_num = random.randint(2345678909800, 9923456789000)

        uniqe_confirm = Order.objects.filter(order_id=random_num)
        # print(random_num)

        while uniqe_confirm:
            random_num = random.randint(234567890980000, 992345678900000)
            if not Order.objects.filter(order_id=random_num):
                break
        # print(random_num)

        user = request.user

        post_order = Order(user=user, order_id=random_num, product_details=prod_details, total_bill=total_money_last,
                           first_name=first_name, last_name=last_name, email=email, phone=phone,
                           country=country, street=street, city=city, zip=zip)
        post_order.save()
        order_id = post_order.order_id
        # print(order_id)

        Thank = True

        return render(request, 'checkout.html', {'Thank': Thank, 'order_id': order_id})

    else:
        user=request.user
        order = Order.objects.filter(user=user, ordered=False)
        if order:
            messages.info(request, 'You Have a Order Remain to Payment !! To Order New, You Have to Pay The first One.')
            return redirect('payment')
        else:
            return render(request, 'checkout.html')
        # return render(request, 'checkout.html')

class PaymentView(View):
    def get(self, args, *kwargs):

        user = self.request.user
        order = Order.objects.get(user=user, ordered=False)


        last_api_get = Stripe_Api.objects.last()
        var_Publishable_key = last_api_get.Publishable_key

        context = {
            'order': order,
            "DISPLAY_COUPON_FORM": False,
            'var_Publishable_key':var_Publishable_key

        }
        return render(self.request, 'payment.html', context)

    def post(self, args, *kwargs):

        last_api_get = Stripe_Api.objects.last()

        stripe.api_key = last_api_get.Secret_key

        print(self.request.user)

        user=self.request.user
        order = Order.objects.get(user=user, ordered=False)

        try:
            customer = stripe.Customer.create(
                email=self.request.user.email,
                description=self.request.user.username,
                source=self.request.POST['stripeToken']
            )
            amount = int(order.total_bill)
            charge = stripe.Charge.create(
                amount=(amount * 100),
                currency="usd",
                customer=customer,
                description="Payment for Fabmom online",
            )

            order.ordered = True

            order.save()

            order_id=order.order_id

            email_for_buy = render_to_string(
                'email_for_buy.html',
                {
                    'order_id': order_id,
                    'first_name': self.request.user.first_name,
                    'last_name': self.request.user.last_name,
                    'prod_details': order.product_details,
                    'total_bill': order.total_bill,
                    'street': order.street,
                    'city': order.city,
                    'postal_code': order.zip,
                    'country': order.country,
                    'phone': order.phone,
                    'email': order.email,
                }
            )
            email=order.email
            send_mail(
                'Purchase Order',  # subject
                email_for_buy,  # massage
                '',  # from email
                [email],  # to email

                fail_silently=True,
            )



            print('okkk')
            messages.success(self.request, 'Payment was Successfull !!')

        except stripe.error.CardError as e:
            messages.info(self.request, f"{e.error.message}")
            return redirect('landing_page_two')

        except stripe.error.RateLimitError as e:
            messages.info(self.request, f"{e.error.message}")
            return redirect('landing_page_two')
        except stripe.error.InvalidRequestError as e:
            messages.info(self.request, "Invalid Request !")
            return redirect('landing_page_two')
        except stripe.error.AuthenticationError as e:
            messages.info(self.request, "Authentication Error !!")
            return redirect('landing_page_two')
        except stripe.error.APIConnectionError as e:
            messages.info(self.request, "Check Your Connection !")
            return redirect('landing_page_two')
        except stripe.error.StripeError as e:
            messages.info(self.request, "There was an error please try again !")
            return redirect('landing_page_two')
        except Exception as e:
            messages.info(self.request, "A serious error occured we were notified !")
            return redirect('landing_page_two')

        return redirect('landing_page_two')




def loyalty_register(request):
    # var_customer = request.session.get('customer')
    if request.user.is_authenticated:
        # get_customer = User.objects.get(id=var_customer)
        chk_loyalty_id = loyalty_registration_table.objects.filter(Customer=request.user)
        if chk_loyalty_id:
            return redirect('loyalty_discount_page')
        else:
            return render(request, 'loyalty_register.html')
    else:
        messages.error(request, "Please Login first then try again for loyalty registration!")
        return redirect('signup_login')


def promotion_register(request):
    return render(request, 'promotion_register.html')



def submit_loyalty_info(request):
    full_name = request.POST.get('full_name')
    loyalty_email = request.POST.get('loyalty_email')
    loyalty_phone = request.POST.get('loyalty_phone')

    # var_customer = request.session.get('customer')
    # get_customer = User.objects.get(id=var_customer)
    get_customer = request.user

    # make random discount percentage
    dis_percentage = random.randint(5, 15)


    my_unique_code = uuid.uuid4()
    str_code_conv = str(my_unique_code)
    loyality_Coupon_Code = str_code_conv[0:6]

    loyality_Coupon_Code = 'l-'+loyality_Coupon_Code

    uniqe_confirm = loyalty_registration_table.objects.filter(loyality_Coupon_Code=loyality_Coupon_Code)
    # print(random_num)
    while uniqe_confirm:
        my_unique_code = uuid.uuid4()
        str_code_conv = str(my_unique_code)
        loyality_Coupon_Code = str_code_conv[0:7]
        if not loyalty_registration_table.objects.filter(loyality_Coupon_Code=loyality_Coupon_Code):
            break


    counpn_tbl = coupon_rate.objects.all().count()
    if counpn_tbl < 1:
        coupon_r_v = coupon_rate(level_name='Low Loyalty', Discount_rate=10)
        coupon_r_v.save()

        rat_disconte = coupon_r_v.Discount_rate
    else:
        lst_random_coupn = list(coupon_rate.objects.all())
        random_coupn = random.sample(lst_random_coupn, 1)
        for k in random_coupn:
            coupon_r_v = k
            rat_disconte = k.Discount_rate


    s_loyalty_reg = loyalty_registration_table(Customer=get_customer, Full_Name=full_name, Phone_No=loyalty_email, Email_id=loyalty_phone, Coupon_rate=coupon_r_v, Discount_percentage=rat_disconte, loyality_Coupon_Code=loyality_Coupon_Code)
    s_loyalty_reg.save()

    request.session['loyalty_id'] = True
    return redirect('loyalty_discount_page')



def loyalty_discount_page(request):
    # var_customer = request.session.get('customer')
    if request.user.is_authenticated:
        # get_customer = User.objects.get(id=var_customer)

        chk_loyalty_id = loyalty_registration_table.objects.filter(Customer = request.user)
        if chk_loyalty_id:
            chk_loyalty_id = loyalty_registration_table.objects.get(Customer=request.user)
            loyality_Coupon_Code = chk_loyalty_id.loyality_Coupon_Code
            dis_percentage = chk_loyalty_id.Discount_percentage
            context = {'loyality_Coupon_Code': loyality_Coupon_Code, 'dis_percentage': dis_percentage, 'chk_loyalty_id':chk_loyalty_id}
            return render(request, 'loyalty_page.html', context)
        else:
            return redirect('loyalty_register')
    else:
        messages.error(request, "Please Login first then try again for loyalty registration!")
        return redirect('signup_login')



def loyalty_benefit_info(request):
    loyalty_benefit_all = loyalty_benefit_info_table.objects.all()
    print('this is benefit info------------------')
    print(loyalty_benefit_all)
    context = {'loyalty_benefit_all':loyalty_benefit_all}
    return render(request, 'loyalty_benefit_info.html', context)


def promotion_coupon_page(request):

    all_any = any_product_discount.objects.all()
    all_cate = Category_level_discount.objects.all()
    all_specific = Specific_Level_Product_Deals.objects.all()

    context = {'all_any':all_any, 'all_cate':all_cate, 'all_specific':all_specific}

    return render(request, 'promotion_coupon_page.html', context)



@csrf_exempt
def check_coupon(request):
    vr_coupon_code = request.POST.get('vr_coupon_code')

    percentage = False

    check_loyalty = loyalty_registration_table.objects.filter(loyality_Coupon_Code=vr_coupon_code, Customer=request.user)

    check_any_discount = any_product_discount.objects.filter(Promotional_deals_Coupon_Code=vr_coupon_code)

    check_cat_discount = Category_level_discount.objects.filter(Promotional_deals_Coupon_Code=vr_coupon_code)

    check_specific_discount = Specific_Level_Product_Deals.objects.filter(Promotional_deals_Coupon_Code=vr_coupon_code)


    if check_loyalty:
        get_loyalty = loyalty_registration_table.objects.get(loyality_Coupon_Code=vr_coupon_code, Customer=request.user)
        percentage = get_loyalty.Discount_percentage
    elif check_any_discount:
        any_dis = any_product_discount.objects.get(Promotional_deals_Coupon_Code=vr_coupon_code)
        percentage = any_dis.Discount_percentage

    elif check_cat_discount:
        cat_dis = Category_level_discount.objects.get(Promotional_deals_Coupon_Code=vr_coupon_code)
        percentage = cat_dis.Discount_percentage

    elif check_specific_discount:
        specific_dis = Specific_Level_Product_Deals.objects.get(Promotional_deals_Coupon_Code=vr_coupon_code)
        percentage = specific_dis.Discount_percentage


    return HttpResponse(percentage)