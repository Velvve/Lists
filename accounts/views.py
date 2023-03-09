import sys

from django.shortcuts import redirect
from django.core.mail import send_mail
from django.contrib import messages, auth
from accounts.models import Token
from django.urls import reverse


def send_login_email(request):
    """отправляет сообщение для входа в систему"""
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + '?token=' + str(token.uid)
    )
    message_body = f'Use this to log in: \n \n {url}'
    send_mail(
        'Your login link for Superlists',
        message_body,
        'velwe-beck@mail.ru',
        [email],
    )
    messages.success(
        request,
        'Check your email, мы отправили Вам ссылку, \
            которую можно использовать для входа на сайт'
    )
    return redirect('/')


def login(request):
    """зарегистрировать вход в систему"""
    print('login view', file=sys.stderr)
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')
