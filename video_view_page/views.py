from django.shortcuts import render, redirect
from .models import Landing_page_eight_model, Landing_page_eight_model_left, subscribe_app_8

# Create your views here.


def landing_page_eight(request):

    get_left = Landing_page_eight_model_left.objects.last()
    contex = {'get_left':get_left}
    return render(request, 'landing_page_eight.html', contex)
    # return render(request, 'landing_page_eight.html')


def Register_info_for_eight(request):
    # get_left = Landing_page_four_model_left.objects.last()
    # contex = {'get_left':get_left}
    # return render(request, 'landing_page_eight.html', contex)
    name_First_Name = request.POST.get('name_First_Name')
    name_Last_Name = request.POST.get('name_Last_Name')
    name_Email_Address = request.POST.get('name_Email_Address')
    checkbox_position = request.POST.get('checkbox_position')
    if checkbox_position == 'on':
        checkbox_position_o = 'on'
    else:
        print('off')
        checkbox_position_o = 'off'

    k = Landing_page_eight_model(Model_First_Name=name_First_Name, Model_Last_Name=name_Last_Name, Model_Email_Address=name_Email_Address, Model_checked_or_not=checkbox_position_o)
    k.save()
    request.session['session_user_id'] = k.id

    # session_user_id = request.session.get('session_user_id')
    # if session_user_id:
    #     return render(request, 'Register_info_for_eight.html')
    # else:
    #     return redirect('landing_page_eight')
    return redirect('landing_page_eight')


def subscribes_app8(request):
    subscribe_email = request.POST.get('subscribe_email')
    data_subscribe = subscribe_app_8(email=subscribe_email)
    data_subscribe.save()
    return redirect('landing_page_eight')