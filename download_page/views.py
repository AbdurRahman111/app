from django.shortcuts import render, redirect
from .models import Landing_page_seven_model_left, Landing_page_seven_model, subscribe_app_7
# Create your views here.


from django.core.mail import send_mail
from django.template.loader import render_to_string




def landing_page_seven(request):
    session_user_id = request.session.get('session_user_id')
    c=''
    if session_user_id:
        c = 'p'
    get_left = Landing_page_seven_model_left.objects.last()

    contex = {
        'get_left': get_left,
        'c':c,

    }
    return render(request, 'landing_page_seven.html', contex)



import mimetypes
import os
from django.http.response import HttpResponse

def download_file(request):
    if request.method == 'POST':
        name_First_Name = request.POST.get('name_First_Name')
        name_Last_Name = request.POST.get('name_Last_Name')
        name_Email_Address = request.POST.get('name_Email_Address')
        CompanyCountry = request.POST.get('CompanyCountry')
        checkbox_position = request.POST.get('checkbox_position')
        print('checkbox_position')
        print(checkbox_position)
        if checkbox_position == 'on':
            checkbox_position_o = 'on'
        else:
            print('off')
            checkbox_position_o = 'off'

        k = Landing_page_seven_model(Model_First_Name=name_First_Name, Model_Last_Name=name_Last_Name, Model_Email_Address=name_Email_Address, Model_country_Address=CompanyCountry, Model_checked_or_not=checkbox_position_o)
        k.save()
        get_left = Landing_page_seven_model_left.objects.last()
        f = get_left.Model_left_content_top
        l = get_left.Model_left_content_bottom
        h = f + l
        # print('ddddddd')
        # print(h)
        #
        # # Define Django project base directory
        # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # # Define text file name
        # filename = 'test.txt'
        # # Define the full file path
        # filepath = BASE_DIR + '/filedownload/Files/' + filename
        #
        # f = open(filepath, 'w')
        # f.write(h)
        # f.close()
        # # Open the file for reading content
        # path = open(filepath, 'r')
        # # Set the mime type
        # mime_type, _ = mimetypes.guess_type(filepath)
        # # Set the return value of the HttpResponse
        # response = HttpResponse(path, content_type=mime_type)
        # # Set the HTTP header for sending to browser
        # response['Content-Disposition'] = "attachment; filename=%s" % filename
        # # Return the response value
        # return response
        # # return redirect('landing_page_seven')
        request.session['session_user_id'] = k.id

        emal_add=name_Email_Address
        generated_otp_num_str='9998'

        email_for_otp = render_to_string(
            'link_send_email.html',
            {
                'generated_otp_num_str': generated_otp_num_str,

            }
        )

        send_mail(
            'Download link- Thank You',  # subject
            email_for_otp,  # massage
            '',  # from email
            [emal_add],  # to email
            fail_silently=True,
        )


        return redirect('landing_page_seven')
    return redirect('landing_page_seven')

def download_file_from_link(request):
    get_left = Landing_page_seven_model_left.objects.last()
    f = get_left.Model_left_content_top
    l = get_left.Model_left_content_bottom
    h = f + l
    print('ddddddd')
    print(h)

    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    filename = 'test.txt'
    # Define the full file path
    filepath = BASE_DIR + '/filedownload/Files/' + filename

    f = open(filepath, 'w')
    f.write(h)
    f.close()
    # Open the file for reading content
    path = open(filepath, 'r')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response
    # return redirect('landing_page_seven')



def clear_seassion(request):
    request.session.clear()
    return redirect('landing_page_seven')


def subscribes_app7(request):
    subscribe_email = request.POST.get('subscribe_email')
    data_subscribe = subscribe_app_7(email=subscribe_email)
    data_subscribe.save()
    return redirect('landing_page_seven')