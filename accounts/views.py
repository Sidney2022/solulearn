from django.contrib.auth.models import auth
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.password_validation import validate_password
from django.http import JsonResponse
import json
from .models import Profile, PwToken
from django.conf import settings
import os, random
from django.core.mail import EmailMessage
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.template.loader import render_to_string


class SignIn(View):
    def post(self, request, *args, **kwargs):
        username = request.POST['username'].lower().strip()
        password = request.POST['password']
        next_page = request.POST['next']
        print(username, password)
        user = auth.authenticate(username=username, password=password)
        print(user)
        if user:
            if user and user.is_active:
                auth.login(request, user)
                if next_page != 'None':
                    return redirect(next_page)
                else:
                    return redirect('homepage')
            else:
                messages.warning(request, 'account has not been verified')
                return redirect('login')
        else:
            messages.error(request, 'invalid login credentials')
            return redirect('login')
            
    def get(self, request, *args, **kwargs):
        redirect_page = request.GET.get("next")
        if request.user.is_authenticated:
            messages.warning(request, f'You are already logged in')
            return redirect('homepage')
        
        return render(request, 'authentication/login.html', {"redirect_page":redirect_page})


class SignUp(View):
    def post(self, request):
        username = request.POST['username'].lower().strip()
        email = request.POST['email'].lower().strip()
        password = request.POST['password']
        password2 = request.POST['password2']
        context = { "fields": request.POST }
        if Profile.objects.filter(username=username).exists():
            messages.error(request, 'username already exists')
            return render(request, 'authentication/signup.html', context)
        elif Profile.objects.filter(email=email).exists():
            messages.error(request, 'email already exists')
            return render(request, 'authentication/signup.html', context)
        elif password != password2:
            messages.error(request, 'passwords do not match!')
            return render(request, 'authentication/signup.html', context)
        
        try:
            validate_password(password)
            new_user = Profile.objects.create_user(username=username, email=email, password=password)
            new_user.save()
            auth.authenticate(username=username, password=password)
            auth.login(request, new_user)
            return redirect("homepage")
        except Exception as e:
            messages.error(request, str(e))
            return render(request, 'authentication/signup.html', context)
    
    

    def get(self, request):
        # f = os.path.join(settings.BASE_DIR, 'currency.json')
        # with open(f, 'r', encoding='utf-8') as file:
        #     json_data = json.load(file)
        #     data = [({'name':k,'value':v['name'], 'symbol':v['symbol']}) for k,v in json_data.items()]
               
        # context = {
        #     'currencies':data,
        # }
        return render(request, 'authentication/signup.html')


class SignOut(View):
    def get(self, request):
        auth.logout(request)
        messages.info(request, "logged out successfuly")
        return redirect('login')


def reset_password(request):
    # this block should render a page with form to enter email. onsubmit,  a token should be generated and sent to users mail
    if request.method == "POST":
        email = request.POST['email'].lower().strip()
        user_profile = get_object_or_404(Profile, email=email)
        num = random.randint(0, 999999)
        # send_email
        subject = f'Email Confirmation'
        context = {
            'recipient_name': user_profile.username,
            "token":token,

            }
        try:
            html_message = render_to_string('email/payment.html', context)
            plain_message = strip_tags(html_message)
        
            send_mail(
                subject, plain_message, settings.DEFAULT_FROM_EMAIL, [email], html_message=html_message
                )
            token = PwToken.objects.create(token=num, user=user_profile) 
            token.save()
            return redirect('verify-token')
        except Exception as e :
            messages.info(request, 'email could not be sent. please check your network connection and try again. if problem persists, please contact admin') 
            return redirect('reset-pw')

    return render(request, 'authentication/password_reset.html')


def reset_password_verify_token(request):
    # this block should render a page with form to enter email, and token. on submit,  a token should be validated. if valid, redirect to change password view
    if request.method == "POST":
        email = request.POST['email'].lower().strip()
        token = request.POST['token'].strip()
        user_profile = get_object_or_404(Profile, email=email)
        # send_email
        token = PwToken.objects.filter( token=token, user=user_profile).first()
        if not token:
            messages.info(request, 'invalid token') 
            return redirect('set-pw')
        return redirect('set-pw')
        
    return render(request, 'authentication/password_reset.html')







