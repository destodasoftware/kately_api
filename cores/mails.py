from django.core import mail
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_email_order(sale, sender, receiver):
    # body = f"Gunakan nomer {sale.sale_number} untuk mengecek pesanan kamu di " \
    #        f"'{settings.LINK_CHECK_ORDER}'. Terimakasih sudah berbelanja di store kami."
    #
    # send_mail(
    #     'Hai, {}'.format(sale.customer.name),
    #     body,
    #     sender,
    #     [receiver]
    # )

    subject = f'Order {sale.customer.name}'
    html_message = render_to_string('cores/send_email_order.html', {'sale': sale})
    plain_message = strip_tags(html_message)
    from_email = sale.user.email
    to = sale.customer.email

    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)