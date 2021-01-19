# import datetime
# from django.core.management import BaseCommand
#
# from foodanddrink.restaurant.models import Order, Customer
#
#
# class Command(BaseCommand):
#     commands = ['sendreport', ]
#     args = '[command]'
#     help = 'Send monthly report'
#
#     def handle(self, *args, **options):
#         this_time = datetime.datetime.now()
#         this_year = this_time.year
#         this_month = this_time.month
#         # order_reports = Order.objects.filter(date_from__year__gte=this_year).filter(date_from__month_gte=this_month)
#         customer_reports = Customer.objects.all()
#         product_reports = Order.objects.filter(date_from__year__gte=this_year).filter(date_from__month_gte=this_month)\
#             .select_related('order_detail').select_related('product')
