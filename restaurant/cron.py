from datetime import datetime

from django.core.mail import EmailMessage

import environ
from django.db.models import Sum
from django.template.loader import render_to_string

from foodanddrink.foodanddrink.settings import env
from foodanddrink.restaurant.models import Order, Customer

env = environ.Env()
environ.Env.read_env()


def monthly_report():
    mail_subject = "Monthly Report"
    now = datetime.now()

    year = now.year
    last_month = now.month - 1
    if last_month == 0:
        last_month = 12
        year -= 1

    income = Order.objects.filter(date_ordered__year = year, date_ordered__month = last_month, status='f').aggregate(Sum('total_price'))
    new_acc_number = Customer.objects.filter(date_joined__year = year, date_joined__month = last_month, is_active = 1).count()

    message = render_to_string('restaurant/report.html', {
        'month' : last_month,
        'income' : income,
        'new_acc_number' : new_acc_number,
    })
    email = EmailMessage(
        mail_subject, message, to=[env('EMAIL_ADMIN')],
    )
    email.content_subtype = "html"
    email.send()
