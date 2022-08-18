from django.shortcuts import render, redirect, HttpResponse
from .models import Landing_page_four_model, Landing_page_four_model_left, subscribe_app_4
from django.contrib import messages


from django.views.decorators.csrf import csrf_exempt
# Create your views here.

import stripe

stripe.api_key = "sk_test_51IWuSRFzvY3Oon8KHXlURApAt4rjhN1qKfh37Xvcwam0uzfvzZt8o3TJCirb5uFParGlho3a15S6V2s0mZLXsaOg00woMU6Fen"

# Create your views here.


# landing page four start

def landing_page_four(request):
    get_left = Landing_page_four_model_left.objects.last()
    contex = {'get_left':get_left}
    return render(request, 'landing_page_four.html', contex)

def landing_page_four_second_page(request):
    print('sssss')
    if request.method == "GET":
        get_left = Landing_page_four_model_left.objects.last()
        contex = {'get_left': get_left}
        return render(request, 'landing_page_four_2.html', contex)

    else:
        money_amount_and_type = request.POST.get('money_amount')



        print(money_amount_and_type)
        x = money_amount_and_type.split(",")
        print(x)

        money_amount = None
        tkn = None

        len = 0
        for i in x:
            len = len + 1
            if len == 1:
                money_amount = i
            else:
                tkn = i

        print(money_amount)
        print(tkn)

        session_user_id = request.session.get('session_user_id')
        if session_user_id:
            print('session_user_id')
            print(session_user_id)
            money = Landing_page_four_model.objects.get(id=session_user_id)
            money.Mobel_donate_amount = money_amount
            money.save()
            request.session.clear()


        try:
            ml = "monnach111@gmail.com"
            des = "monna"
            customer = stripe.Customer.create(
                email=ml,
                description=des,
                source=tkn
            )
            print('step2')
            amount = int(money_amount)
            print(amount)

            charge = stripe.Charge.create(
                amount=(amount * 100),
                currency="usd",
                customer=customer,
                description="Payment for Donate",
            )
            print("step3")


            messages.success(request, "Your Payment was Successfull !!")
            return redirect('landing_page_four')

        except stripe.error.CardError as e:
            messages.info(request, f"{e.error.message}")
            return redirect('landing_page_four')

        except stripe.error.RateLimitError as e:
            messages.info(request, f"{e.error.message}")
            return redirect('landing_page_four')
        except stripe.error.InvalidRequestError as e:
            messages.info(request, "Invalid Request !")
            return redirect('landing_page_four')
        except stripe.error.AuthenticationError as e:
            messages.info(request, "Authentication Error !!")
            return redirect('landing_page_four')
        except stripe.error.APIConnectionError as e:
            messages.info(request, "Check Your Connection !")
            return redirect('landing_page_four')
        except stripe.error.StripeError as e:
            messages.info(request, "There was an error please try again !")
            return redirect('landing_page_four')
        except Exception as e:
            messages.info(request, "A serious error occured we were notified !")
            return redirect('landing_page_four')




def Register_info_four(request):
    #sob save
    name__Name = request.POST.get('name__Name')
    Email_Address = request.POST.get('Email_Address')
    name_Address = request.POST.get('name_Address')
    checkbox_position = request.POST.get('checkbox_position')
    if checkbox_position == 'on':
        checkbox_position_o = 'on'
    else:
        print('off')
        checkbox_position_o = 'off'

    k = Landing_page_four_model(Mobel_Name=name__Name, Mobel_Email_Address=Email_Address, Mobel_Address=name_Address, Model_checked_or_not=checkbox_position_o)
    k.save()
    request.session['session_user_id'] = k.id

    return redirect('landing_page_four_second_page')


def subscribes_app4(request):
    subscribe_email = request.POST.get('subscribe_email')
    data_subscribe = subscribe_app_4(email=subscribe_email)
    data_subscribe.save()
    return redirect('landing_page_four')