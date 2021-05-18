import os
from mailjet_rest import Client
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.html import strip_tags
from django.template.loader import render_to_string


def send_verification_email(profile):
    # UNCOMMENT WHEN UI FOR ACCOUNT VERIFICATION BY ADMIN IS CREATED
    # current_site = get_current_site(request)
    # protocol = 'https' if request.is_secure() else 'http'
    current_site_domain = 'sac.iiitdmj.ac.in'
    protocol = 'http'

    rendered_url = render_to_string('registration/url_password_reset_email.html', {
        'uid': urlsafe_base64_encode(force_bytes(profile.user.pk)),
        'user': profile.user,
        'token': default_token_generator.make_token(profile.user),
        # 'domain': current_site.domain,
        'domain': current_site_domain,
        'protocol': protocol,
    })

    from_email = settings.DEFAULT_FROM_EMAIL
    to = [profile.email]

    subject = 'SAC IIITDMJ Portal Registration Successful!'

    html_message = render_to_string('registration/account_verification_email.html', {
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
        [settings.BCC_EMAIL_ID],
    )
    email.attach_alternative(html_message, "text/html")

    print("sending email to {}".format(to))
    try:
        email.send()
    except Exception as error:
        print("Exception while sending mail to {}".format(to))
        print(error)


def send_verification_email_old(user, name, email, yoa, yop, prog, spec, reg_no, roll):
    c = {
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'user': user,
        'token': default_token_generator.make_token(user),
        'domain': 'sac.iiitdmj.ac.in',  # request.META['HTTP_HOST'],
        'protocol': 'http',
    }
    url_template_name = 'registration/url_password_reset_email.html'
    api_key = os.environ['MJ_APIKEY_PUBLIC']
    api_secret = os.environ['MJ_APIKEY_PRIVATE']
    sender_email = os.environ['MJ_SENDER_EMAIL']
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
        'Messages': [
            {
                "From": {
                    "Email": sender_email,
                    "Name": "Student Alumni Cell (SAC), IIITDMJ"
                },
                "To": [
                    {
                        "Email": email,
                        "Name": name
                    }
                ],
                "Bcc": [
                    {
                        "Email": "dean.s@iiitdmj.ac.in",
                        "Name": "Dean Students"
                    }
                ],
                "TemplateID": 821551,
                "TemplateLanguage": True,
                "Subject": "SAC IIITDMJ Portal Registration Successful!",
                "TemplateErrorDeliver": True,
                "TemplateErrorReporting": {
                    "Email": sender_email,
                    "Name": "Error in Message Delivery - SAC"
                },
                "Variables": {
                    "name": name,
                    "email": email,
                    "from": yoa,
                    "to": yop,
                    "prog": prog,
                    "branch": spec,
                    "reg_no": reg_no,
                    "roll_no": roll,
                    "pass": render_to_string(url_template_name, c)
                }
            }
        ]
    }
    result = mailjet.send.create(data=data)
    return result.status_code


def send_birthday_wish(name, email):
    api_key = os.environ['MJ_APIKEY_PUBLIC']
    api_secret = os.environ['MJ_APIKEY_PRIVATE']
    sender_email = os.environ['MJ_SENDER_EMAIL']
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
        'Messages': [
            {
                "From": {
                    "Email": sender_email,
                    "Name": "Student Alumni Cell (SAC), IIITDMJ"
                },
                "To": [
                    {
                        "Email": email,
                        "Name": name
                    }
                ],
                "Bcc": [
                    {
                        "Email": "dean.s@iiitdmj.ac.in",
                        "Name": "Dean Students"
                    }
                ],
                "TemplateID": 820446,
                "TemplateLanguage": True,
                "Subject": "Student Alumni Cell, IIITDMJ Wishes you a Very Happy Birthday!",
                "TemplateErrorDeliver": True,
                "TemplateErrorReporting": {
                    "Email": sender_email,
                    "Name": "Error in Message Delivery - SAC"
                },
                "Variables": {
                    "firstname": name,
                }
            }
        ]
    }
    result = mailjet.send.create(data=data)
    return result.status_code
