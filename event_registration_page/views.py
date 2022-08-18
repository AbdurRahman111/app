from django.shortcuts import render, redirect
from .models import Landing_page_five_model_left, Landing_page_five_event, Landing_page_five_model, subscribe_app_5
# Create your views here.
from django.contrib import messages

# Create your views here.
def landing_page_five(request):
    get_left = Landing_page_five_model_left.objects.last()
    get_event = Landing_page_five_event.objects.all()
    contex = {
        'get_left': get_left,
        'get_event': get_event,
              }
    return render(request, 'landing_page_five.html', contex)

def Register_info_for_five(request):
    if request.method == 'POST':
        name_First_Name = request.POST.get('name_First_Name')
        name_Last_Name = request.POST.get('name_Last_Name')
        name_Email_Address = request.POST.get('name_Email_Address')
        checkbox_position = request.POST.get('checkbox_position')
        if checkbox_position == 'on':
            checkbox_position_o = 'on'
        else:
            print('off')
            checkbox_position_o = 'off'

        k = Landing_page_five_model(Model_First_Name=name_First_Name, Model_Last_Name=name_Last_Name, Model_Email_Address=name_Email_Address, Model_checked_or_not=checkbox_position_o)
        k.save()

        messages.warning(request, 'Successfully Saved')
        return redirect('landing_page_five')

    return redirect('landing_page_five')

def subscribes_app5(request):
    subscribe_email = request.POST.get('subscribe_email')
    data_subscribe = subscribe_app_5(email=subscribe_email)
    data_subscribe.save()
    return redirect('landing_page_five')