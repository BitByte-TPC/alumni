from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import Context, Template
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.html import strip_tags

from datetime import date, datetime

from applications.alumniprofile.models import Profile
from applications.events_news.models import Event
from .models import EmailTemplate, EmailHistory

import pytz

ALLOWED_RECIPIENTS_PER_DAY = 500


def is_superuser(user):
    return user.is_superuser


 
def get_rendered_emails(from_email, email_template, recipients):
    subject = email_template.subject

    body = email_template.body
    body_template = Template(body)

    messages = []
    bcc=settings.BCC_EMAILS

    for profile in recipients:  
        bcc.append(profile.email)

    context = Context({
            "profile": profile,
        })

    html_message = body_template.render(context)
    plain_message = strip_tags(html_message)
    
    email = EmailMultiAlternatives(
            subject,
            plain_message,
            from_email,
            ['alumni@iiitdmj.ac.in'],
            bcc ,
            # settings.BCC_EMAILS,
        )
    email.attach_alternative(html_message, "text/html")
    messages.append(email)

    return messages
    
@login_required
@user_passes_test(
    is_superuser, redirect_field_name=None,
    login_url=reverse_lazy('home')
)
def index(request):
    return render(request, 'adminportal/index.html')


#Function to convert datetime from naive to offset
def convert_datetime_to_offset(naive_time):
    timezone = pytz.timezone("UTC")
    offset_time = timezone.localize(datetime.strptime(naive_time, '%Y-%m-%dT%H:%M'))
    return offset_time


#Function to convert datetime from offset to naive
def convert_datetime_to_naive(offset_time):
    offset_time = str(offset_time)
    naive_time = offset_time[:10] + "T" +  offset_time[11:-6]
    return naive_time


@login_required
@user_passes_test(
    is_superuser, redirect_field_name=None,
    login_url=reverse_lazy('home')
)
def events(request):
    if request.method == 'POST':
        try:
            title = request.POST['title']
            description = request.POST['description']
            start_date_time = request.POST['start_date_time']
            end_date_time = request.POST['end_date_time']
            address = request.POST['address']
            location = request.POST['location']
            by = request.POST['organiser']
            picture = request.FILES.get('cover_image')
            
            start_date_time = convert_datetime_to_offset(start_date_time)
            end_date_time = convert_datetime_to_offset(end_date_time)

            if(end_date_time <= start_date_time):
                messages.error(request, f"Start date & time should be less than end date & time.")
                return redirect('adminportal:events')

            event = Event(
                title = title,
                description = description,
                location = location,
                address = address,
                by = by,
                start_date = start_date_time,
                end_date = end_date_time
            )
            
            event.save()
            if(picture != None):
                event.picture = picture
                event.save()

        except Exception as err:
            messages.add_message(request, messages.ERROR, err)
            return redirect('adminportal:events')

    return render(request, 'adminportal/events.html')


@login_required
@user_passes_test(
    is_superuser, redirect_field_name=None,
    login_url=reverse_lazy('home')
)
def registrations_index(request):
    if request.method == 'POST':
        try:
            profile = Profile.objects.get(roll_no=request.POST.get('id'))
            if profile.verify is not None:
                raise RuntimeError("Invalid verification request for roll no. {}.".format(profile.roll_no))

            if 'approve' in request.POST:
                profile.verify = True
                # mail_sent = send_verification_email(get_current_site(request).domain, request.is_secure(), profile)
                # profile.mail_sent = mail_sent
                profile.save()

                # To check if mail_sent was also updated
                profile.refresh_from_db()
                if profile.mail_sent:
                    messages.add_message(request, messages.SUCCESS, "Registration Success, Mail sent to {}".format(profile.name))
                else:
                    messages.add_message(request, messages.ERROR, "Something went wrong. Verification mail not sent to {}".format(profile.name))

            elif 'decline' in request.POST:
                profile.verify = False
                profile.save()
                messages.add_message(request, messages.SUCCESS, "Registration Declined for {}".format(profile.name))

        except Exception as err:
            print(err)
            messages.add_message(request, messages.ERROR, err)

        return redirect('adminportal:registrations')

    unregistered = Profile.objects.filter(verify=None).filter(mail_sent=False).order_by('-user__date_joined')

    context = {
        'pending': unregistered
    }
    return render(request, 'adminportal/registrations.html', context)


@login_required
@user_passes_test(
    is_superuser, redirect_field_name=None,
    login_url=reverse_lazy('home')
)
def mailservice_index(request):
    programmes = Profile.objects.values_list('programme', flat=True).distinct()
    batches = Profile.objects.select_related('batch').values_list('batch__batch', flat=True).distinct()
    branches = Profile.objects.values_list('branch', flat=True).distinct()

    if request.method == 'POST':
        template_id = request.POST['template_id']
        programme = request.POST['programme']
        batch = request.POST['batch']
        branch = request.POST['branch']

        template = EmailTemplate.objects.get(template_id=template_id)
        recipients = Profile.objects.all()

        if programme:
            recipients = recipients.filter(programme=programme)
        if batch:
            recipients = recipients.filter(batch__batch=batch)
        if branch:
            recipients = recipients.filter(branch=branch)

        total_recipients = recipients.count()
        if total_recipients == 0:
            messages.error(request, f"Cannot send email to 0 recipients.")
            return redirect('adminportal:mailservice')

        emails_sent_today = EmailHistory.objects.filter(
            timestamp__date=date.today()
        ).aggregate(Sum('total_delivered'))['total_delivered__sum']

        if emails_sent_today is None:
            emails_sent_today = 0

        total_recipients_allowed = ALLOWED_RECIPIENTS_PER_DAY - emails_sent_today
        if total_recipients > total_recipients_allowed:
            messages.error(request, f"You can only send {total_recipients_allowed} more emails today. Limit: 500 per day.")
            return redirect('adminportal:mailservice')

        email_messages = get_rendered_emails(settings.DEFAULT_FROM_EMAIL, template, recipients)

        try:
            connection = mail.get_connection()
            total_messages_delivered = connection.send_messages(email_messages)
            EmailHistory.objects.create(
                email_template=template.name,
                programme=programme if programme else ', '.join(programmes),
                batch=batch if batch else ', '.join(map(str, batches)),
                branch=branch if branch else ', '.join(branches),
                total_recipients=total_recipients,
                total_delivered=total_messages_delivered,
            )
        except Exception as error:
            print(error)
            messages.error(request, "Something went wrong while sending the emails.")
            return redirect('adminportal:mailservice')

        messages.success(request, f"Email sent successfully to {total_messages_delivered} recipients.")
        return redirect('adminportal:mailservice')

    email_templates = EmailTemplate.objects.all()
    email_history = EmailHistory.objects.all().order_by('-timestamp')

    context = {
        'email_templates': email_templates,
        'email_history': email_history,
        'programmes': programmes,
        'batches': batches,
        'branches': branches,
    }

    return render(request, 'adminportal/mailservice.html', context)
