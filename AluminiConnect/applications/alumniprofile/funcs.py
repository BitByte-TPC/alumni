import os
from mailjet_rest import Client
from django.contrib import messages

def send_verification_email(name, email, yoa, yop, prog, spec, reg_no):
    try:
        api_key = os.environ['MJ_APIKEY_PUBLIC']
        api_secret = os.environ['MJ_APIKEY_PRIVATE']
        sender_email = os.environ['MJ_SENDER_EMAIL']
    except:
        return ("Not Sent")
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
                        "Subject": "IIITDMJ SAC Portal Registration",
                        "TextPart": "Dear Alumni, Thanks for Registering on the SAC Portal, IIITDMJ!",
                        "HTMLPart": "<h3>Dear Alumni, Thanks for Registering on the SAC Portal, IIITDMJ! You've been verified by the Admin.</h3>\
                                <h3> <u>Details</u><br>Name : {}<br>Email : {}<br>Batch : {} - {}<br>Programme : {}<br>Branch : {}<br><u>Alumni Registration Number : {}</u></h3>\
                                    <p> Please use this number for future references and endeavours.<br>\
                                        Apply for Alumni Card - <a href=\"https://forms.gle/5AwdnQjyuwUp5K2h8/\">Link</a></p>".format(name,email,yoa,yop,prog,spec,reg_no)
                                    
                    }
            ]
    }
    result = mailjet.send.create(data=data)
    return (result.status_code)
    