import datetime
import hashlib
from core.models import *
from django.conf import settings
from .c2b import C2B
from .b2b import B2B
from .utils import *
from api import AfricasTalkingGateway
from api.AfricasTalkingGateway import AfricasTalkingGatewayException
from api.AfricasTalkingGateway import AfricasTalkingGateway
from django.utils import timezone
import pytz

def initiateB2BTransaction(partyB, amount, account_reference):
    print ("initiateB2BTransaction")
    b2b = B2B(env=settings.ENV)
    try:
        res = b2b.transact(initiator='apitest361', security_credential='361reset', command_id='MerchantToMerchantTransfer', sender_identifier_type='4',
                 receiver_identifier_type='4', amount=500, party_a=174379, party_b=partyB, remarks='None',
                 account_reference='254703421124', queue_timeout_url='https://putsreq.com/C1HAyC3fEEbl2UaEu6lU', result_url=settings.MPESA_B2B_RESULT_URL)   
        # transaction = Transaction(recipient=partyB, 
        #     successful=True, 
        #     reference_number=account_reference, 
        #     amount=amount,
        #     time=datetime.datetime.now())
        # transaction.save()
        print (f'Response: {res}')
        return res

    except Exception as e:
        print ('Encountered an error while posting: %s' % str(e) )

def initiateC2BTransaction(phone_no, amount):
    print ("initiateC2BTransaction")
    passwordBytes = base64.b64encode("174379.bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919.20190903174325".encode('utf-8'))
    password = str(passwordBytes, "utf-8")
    print(password)
    c2b = C2B(env='sandbox')
    # registerC2b = c2b.register(shortcode='174379', response_type='Default', confirmation_url='https://peternjeru.co.ke/safdaraja/api/confirmation.php', validation_url='https://peternjeru.co.ke/safdaraja/api/validation.php')
    # print (f'registerC2b {registerC2b}')
    res = c2b.simulate(shortcode=174379, command_id='CustomerPayBillOnline', amount=amount, msisdn=format_mpesa_number(phone_no), bill_ref_number='account')
    print (f'res_json {res}')
    return res


def send_sms(phone, sms, message_type, content_id):
    outbox = Outbox(recipient=phone, message=sms, message_type=message_type, msg_content_id=content_id, sent=False)
    gateway = AfricasTalkingGateway()

    # Any gateway errors will be captured by our custom Exception class below,
    # so wrap the call in a try-catch block
    try:
        # That's it, hit send and we'll take care of the rest.
        #using test phone number in dev
        print(f"send_sms: {format_africastalking_number('+254799987789')}")
        results = gateway.sendMessage(format_africastalking_number('+254799987789'), sms)
        print(results)
        message_data = results['SMSMessageData']
        recipients = message_data['Recipients'] 
        for recipient in recipients:
            # Status is either "Success" or "error message"
            print ('number=%s;status=%s;messageId=%s;cost=%s' % (recipient['number'],
                                                                recipient['status'],
                                                                recipient['messageId'],
                                                                recipient['cost']) )
            if recipient['status'] == "Success":
                outbox.sent_time = timezone.now()
                outbox.sent = True
                outbox.ait_message_id = recipient['messageId']
            else:
                outbox.sent = False
                outbox.ait_message_id = recipient['messageId']
            outbox.save()
    except Exception:
        print ('Encountered an error while sending: %s' % str(AfricasTalkingGatewayException) )


# @background(schedule=10)
def send_reset_password(phone_number, password, user_id):
    message = "Your new password is: {0}".format(password)
    send_sms(phone_number, message, "Password Reset", user_id)

def send_registration_sms(phone_number, code, id):
    message = f"Hello, Your one time registration code is: {code}"
    send_sms(phone_number, message, "Loanee Registration", id)

def send_registration_welcome(loanee):
    message = f"Welcome to Habahaba {loanee.first_name}"
    send_sms(loanee.phone_number, message, "Loanee Registration", id)
