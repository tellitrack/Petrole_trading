import time
from sinchsms import SinchSMS
from messaging_interface import MessagingInterface


class SMSSender(MessagingInterface):
    def __init__(self, app_key, app_secret, number):
        self.client = SinchSMS(app_key, app_secret)
        self.number = number

    def send(self, recipient, message):
        print("Sending '%s' to %s" % (message, recipient))
        response = self.client.send_message(recipient, message)
        message_id = response['messageId']
        response = self.client.check_status(message_id)

        while response['status'] != 'Successful':
            print(response['status'])
            time.sleep(1)
            response = self.client.check_status(message_id)

        print(response['status'])


if __name__ == '__main__':
    sms_sender = SMSSender(app_key='your_app_key', app_secret='your_app_secret', number='your_phone_number')
    sms_sender.send(recipient='recipient_phone_number', message="Hello from SMS Sender!")
