from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import Context, Template
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode

from applications.alumniprofile.models import Profile
from .models import EmailTemplate


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
            [settings.BCC_EMAIL_ID],
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

        messages = get_rendered_emails(settings.DEFAULT_FROM_EMAIL, template, recipients)

        connection = mail.get_connection(fail_silently=True)
        connection.send_messages(messages)

        return redirect('mailservice:email_sent')

    email_templates = EmailTemplate.objects.all()
    programmes = Profile.objects.values_list('programme', flat=True).distinct()
    batches = Profile.objects.select_related('batch').values_list('batch__batch', flat=True).distinct()
    branches = Profile.objects.values_list('branch', flat=True).distinct()

    context = {
        'email_templates': email_templates,
        'programmes': programmes,
        'batches': batches,
        'branches': branches,
    }

    return render(request, 'mailservice/index.html', context)


def email_sent(request):
    return render(request, 'mailservice/success.html')
