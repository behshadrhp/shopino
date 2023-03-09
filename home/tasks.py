from time import sleep
from celery import shared_task


@shared_task
def notification_customer(message):
    print('Sending 10k mails...')
    print(message)
    sleep(10)
    print('Email were successfully sent!')
