from celery import shared_task
from celery.utils.log import get_task_logger
from datetime import date

from .models import Profile
from .funcs import send_birthday_wish

logger = get_task_logger(__name__)


@shared_task
def send_birthday_wishes():
    today = date.today()
    birthday_users = Profile.objects.filter(date_of_birth__day=today.day, date_of_birth__month=today.month)
    if birthday_users:
        logger.info("{} People have birthdays today".format(len(birthday_users)))
        for user in birthday_users:
            # send_birthday_wish(user.name, user.email)
            logger.info("Mail Sent to {} at {}".format(user.name, user.email))
        logger.info("Mail Sent to {} People Today!".format(len(birthday_users)))
    else:
        logger.info("No Birthdays Today!")
