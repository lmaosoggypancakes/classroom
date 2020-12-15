from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from .ip import get_ip
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import PasswordReset, User
import hashlib
from .models import PasswordReset, User
def reset_pw(request, email):
    ip = get_ip(request)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    hashed_code = hashlib.sha256()
    hashed_code.update(bytes(email, encoding="utf-8"))
    user = PasswordReset()
    user.for_user = User.objects.get(email=email)
    user.hashed_code = hashed_code.hexdigest()
    user.save()
    subject = f'Reset Password for {email}'
    html_message = render_to_string('classroom/email.html', {'hash': hashed_code.hexdigest()})
    plain_message = strip_tags(html_message)
    to = email
    send_mail(subject, plain_message, email_from, recipient_list, html_message=html_message)