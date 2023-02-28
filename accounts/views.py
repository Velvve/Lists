from django.shortcuts import redirect
from django.core.mail import send_mail


def send_login_email(request):
    """отправляет сообщение для входа в систему"""
    email = request.POST['email']
    send_mail(
        'Your login link for Superlists',
        'body text tbc',
        'velwe-beck@mail.ru',
        [email],
     )
    return redirect('/')
