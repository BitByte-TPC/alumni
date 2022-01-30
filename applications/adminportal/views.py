from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import Context, Template
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode

from datetime import date

from applications.alumniprofile.models import Profile
from .models import EmailTemplate, EmailHistory


ALLOWED_RECIPIENTS_PER_DAY = 500


def is_superuser(user):
    return user.is_superuser


def get_rendered_emails(from_email, email_template, recipients):
    subject = email_template.subject

    body = email_template.body
    body_template = Template(body)

    messages = []

    for profile in recipients:
        context = Context({
            "profile": profile,
        })
        html_message = body_template.render(context)
        plain_message = strip_tags(html_message)

        email = EmailMultiAlternatives(
            subject,
            plain_message,
            from_email,
            [profile.email],
            settings.BCC_EMAILS,
        )
        email.attach_alternative(html_message, "text/html")
        messages.append(email)

    return messages


def send_verification_email(request, profile):
    current_site = get_current_site(request)
    protocol = 'https' if request.is_secure() else 'http'

    rendered_url = render_to_string('registration/url_password_reset_email.html', {
        'uid': urlsafe_base64_encode(force_bytes(profile.user.pk)),
        'user': profile.user,
        'token': default_token_generator.make_token(profile.user),
        'domain': current_site.domain,
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
    except Exception as error:
        print("Exception while sending mail to {}".format(to))
        print(error)


@login_required
@user_passes_test(
    is_superuser, redirect_field_name=None,
    login_url=reverse_lazy('home')
)
def index(request):
    return render(request, 'adminportal/index.html')


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
                raise RuntimeError("Invalid Verification request for {}".format(profile.roll_no))

            if 'approve' in request.POST:
                send_verification_email(request, profile)
                profile.mail_sent = True
                profile.verify = True
                messages.add_message(request, messages.SUCCESS, "Registration Success, Mail sent to {}".format(profile.name))

            elif 'decline' in request.POST:
                profile.verify = False
                messages.add_message(request, messages.SUCCESS, "Registration Declined for {}".format(profile.name))

            profile.save()
        except Exception:
            print(Exception)
            messages.add_message(request, messages.ERROR, "Something went wrong, contact the admins.")

        return redirect('adminportal:registrations')

    unregistered = Profile.objects.all().filter(verify=None).filter(mail_sent=False)

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
