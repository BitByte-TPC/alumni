import os
from mailjet_rest import Client
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader

def send_verification_email(user, name, email, yoa, yop, prog, spec, reg_no, roll):
    c = {
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'user': user,
        'token': default_token_generator.make_token(user),
        'domain': 'sac.iiitdmj.ac.in',#request.META['HTTP_HOST'],
        'protocol': 'http',
    }
    url_template_name='registration/url_password_reset_email.html'
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
                        "Variables" : {
                            "name" : name,
                            "email" : email,
                            "from" : yoa,
                            "to" : yop,
                            "prog" : prog,
                            "branch" : spec,
                            "reg_no" : reg_no,
                            "roll_no" : roll,
                            "pass" : loader.render_to_string(url_template_name, c)
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
                        "Variables" : {
                            "firstname" : name,
                        }
                    }
            ]
    }
    result = mailjet.send.create(data=data)
    return result.status_code