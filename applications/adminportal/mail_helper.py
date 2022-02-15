from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode

def send_verification_email(domain, secure_request, profile):
    protocol = 'https' if secure_request else 'http'

    rendered_url = render_to_string('registration/url_password_reset_email.html', {
        'uid': urlsafe_base64_encode(force_bytes(profile.user.pk)),
        'user': profile.user,
        'token': default_token_generator.make_token(profile.user),
        'domain': domain,
        'protocol': protocol,
    })

    from_email = settings.DEFAULT_FROM_EMAIL
    to = [profile.email]

    subject = 'Alumni Connect Portal - IIITDMJ Registration Successful!'

    html_message = render_to_string('registration/account_verification_email_old.html', {
        "name" : profile.name,
        "email" : profile.email,
        "from" : profile.year_of_admission,
        "to" : profile.batch.batch,
        "prog" : profile.programme,
        "branch" : profile.branch,
        "reg_no" : profile.reg_no,
        "roll_no" : profile.roll_no,
        "pass" : rendered_url,
    })
    plain_message = strip_tags(html_message)

    email = EmailMultiAlternatives(
        subject,
        plain_message,
        from_email,
        to,
        settings.BCC_EMAILS,
    )
    email.attach_alternative(html_message, "text/html")

    print("sending email to {}".format(to))
    try:
        email.send()
        return True
    except Exception as error:
        print("Exception while sending mail to {}".format(to))
        print(error)
        return False