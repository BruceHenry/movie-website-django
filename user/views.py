from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import UserCreateForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib import messages #import messages
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate, logout

from verify_email.email_handler import send_verification_email
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator

from django.urls import reverse

# UserModel = get_user_model()

# Create your views here.
@csrf_protect
def user_login(request):
    if request.POST:
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        user = authenticate(username=user_name, password=pass_word)
        print('None', user)
        if user is not None and user.is_active:
            print("User Login:  Username:" + user_name + '    Password:' + pass_word)
            print(request.POST)
            login(request, user)
            return redirect(request.POST.get('path'))
        else:
            return render(request, 'base.html', {'message': 'Username or Password wrong!'})
    else:
        return render(request, '404.html')

@csrf_protect
def user_logout(request):
    logout(request)
    return redirect('/')

#complete register page
@csrf_protect
def user_register(request):
    if request.method=="POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your  account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = UserCreateForm()
    return render(request, template_name="register.html", context={"register_form": form})


def activate(request, uidb64):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None:
        user.backend = 'django.contrib.auth.backends.ModelBackend' 
        # print('In ra o day nhe ')
        user.is_active = True
        user.save()
        # print(user.is_active)
        # print(user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account. \
        Login <a href = "http://localhost:8000/"> Here </a> ')
    else:
        return HttpResponse('Activation link is invalid!')

#complete Facebook
def facebook(request):
    print('chuyen toi day !!!!')
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        login(request, user)
    else:
        # Create new account with default password
        user = User.objects.create_user(username=username, password='facebook')
        user.save()
        user = authenticate(username=username, password='facebook')
        login(request, user)
    return HttpResponse()

def user_detail(request, format=None):
    print('co goi den day khong !!!')
    username = request.user.get_username()
    return render(request, "user_detail.html", {'username': username})