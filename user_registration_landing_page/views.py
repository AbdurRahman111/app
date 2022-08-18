from django.shortcuts import render, redirect, HttpResponse
from .models import Landing_page_one_model, Landing_page_one_model_left, subscribe_app1
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import stripe

stripe.api_key = "sk_test_51IWuSRFzvY3Oon8KHXlURApAt4rjhN1qKfh37Xvcwam0uzfvzZt8o3TJCirb5uFParGlho3a15S6V2s0mZLXsaOg00woMU6Fen"

# landing page one start
def landing_page_one(request):
    get_left = Landing_page_one_model_left.objects.last()
    contex = {'get_left':get_left}
    return render(request, 'landing_page_one.html', contex)

def Register_info(request):
    name_First_Name = request.POST.get('name_First_Name')
    name_Last_Name = request.POST.get('name_Last_Name')
    name_Email_Address = request.POST.get('name_Email_Address')
    name_Date_of_Birth = request.POST.get('name_Date_of_Birth')
    name_City = request.POST.get('name_City')
    name_State = request.POST.get('name_State')
    name_Zip_Code = request.POST.get('name_Zip_Code')
    checkbox_position = request.POST.get('checkbox_position')
    if checkbox_position == 'on':
        checkbox_position_o = 'on'
    else:
        print('off')
        checkbox_position_o = 'off'

    k = Landing_page_one_model.objects.filter(Mobel_Email_Address=name_Email_Address)
    if k:
        pass
    else:
        get_value_of_model = Landing_page_one_model(Mobel_First_Name=name_First_Name, Mobel_Last_Name=name_Last_Name, Mobel_Email_Address=name_Email_Address, Mobel_Date_of_Birth=name_Date_of_Birth, Mobel_City=name_City, Mobel_State=name_State, Mobel_Zip_Code=name_Zip_Code, Model_checked_or_not=checkbox_position_o)
        get_value_of_model.save()
        messages.warning(request, 'Successfully Saved')
    return redirect('landing_page_one')




@csrf_exempt
def check_Email_Address_is_exist(request):
    email = request.POST.get('x')
    is_it = Landing_page_one_model.objects.filter(Mobel_Email_Address=email)
    if is_it and email != '' and email != 'none':
        return HttpResponse('Exist')
    else:
        return HttpResponse('New')
# landing page one end



def subscribes_app2(request):
    subscribe_email = request.POST.get('subscribe_email')

    data_subscribe = subscribe_app1(email=subscribe_email)
    data_subscribe.save()
    return redirect('landing_page_one')






