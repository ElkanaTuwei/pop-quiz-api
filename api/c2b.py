import requests
from .auth import MpesaBase
import base64
import datetime
from django.conf import settings

class C2B(MpesaBase):
    def __init__(self, env="sandbox"):
        MpesaBase.__init__(self, env)
        self.authentication_token = self.authenticate()
        self.passKey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'

    def register(self, shortcode=None, response_type=None, confirmation_url=None, validation_url=None):
        """This method uses Mpesa's C2B API to register validation and confirmation URLs on M-Pesa.

                                    **Args:**
                                        - shortcode (int): The short code of the organization.
                                        - response_type (str): Default response type for timeout. Incase a tranaction times out, Mpesa will by default Complete or Cancel the transaction.
                                        - confirmation_url (str): Confirmation URL for the client.
                                        - validation_url (str): Validation URL for the client.


                                    **Returns:**
                                        - OriginatorConverstionID (str): The unique request ID for tracking a transaction.
                                        - ConversationID (str): The unique request ID returned by mpesa for each request made
                                        - ResponseDescription (str): Response Description message


        """

        payload = {
            "ShortCode": shortcode,
            "ResponseType": response_type,
            "ConfirmationURL": settings.MPESA_REGISTER_CONFIRMATION_URL,
            "ValidationURL": settings.MPESA_REGISTER_VALIDATION_URL,
            "ResultURL": settings.MPESA_REGISTER_RESULT_URL,
            "CallBackURL": settings.MPESA_REGISTER_CALLBACK_URL
        }
        headers = {'Authorization': 'Bearer {0}'.format(self.authentication_token), 'Content-Type': "application/json"}
        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        saf_url = "{0}{1}".format(base_safaricom_url, "/mpesa/c2b/v1/registerurl")
        r = requests.post(saf_url, headers=headers, json=payload)
        return r.json()

    def simulate(self, shortcode=None, command_id=None, amount=None, msisdn=None, bill_ref_number=None):
        """This method uses Mpesa's C2B API to simulate a C2B transaction.

                                            **Args:**
                                                - shortcode (int): The short code of the organization.
                                                - command_id (str): Unique command for each transaction type. - CustomerPayBillOnline - CustomerBuyGoodsOnline.
                                                - amount (int): The amount being transacted
                                                - msisdn (int): Phone number (msisdn) initiating the transaction MSISDN(12 digits)
                                                - bill_ref_number: Optional


                                            **Returns:**
                                                - OriginatorConverstionID (str): The unique request ID for tracking a transaction.
                                                - ConversationID (str): The unique request ID returned by mpesa for each request made
                                                - ResponseDescription (str): Response Description message


        """
        timeStamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        password_string = f"{shortcode}{self.passKey}{timeStamp}".encode('UTF-8')
        # passwordBytes = base64.encodestring(password_string.digest)
        # password = str(passwordBytes, "utf-8")
        # print(passwordBytes)

        passwordBytes = base64.b64encode(password_string)
        password = str(passwordBytes, "UTF-8")
        print(password)
        payload = {
            "BusinessShortCode": shortcode,
            "Password": password,
            "Timestamp": timeStamp,
            "TransactionType": command_id,
            "CommandID": command_id,
            "Amount": amount,
            "PartyA": msisdn,
            "PartyB": shortcode,
            "PhoneNumber": msisdn,
            "BillRefNumber": bill_ref_number,
            "AccountReference": "HabaHaba",
            "TransactionDesc": "deposit",
            "ResultURL": settings.MPESA_C2B_RESULT_URL,
            "CallBackURL": settings.MPESA_C2B_CALLBACK_URL
        }
        headers = {'Authorization': 'Bearer {0}'.format(self.authentication_token), 'Content-Type': "application/json"}
        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        saf_url = "{0}{1}".format(base_safaricom_url, "/mpesa/stkpush/v1/processrequest")
        # saf_url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        print(saf_url)
        print(f'{headers}')
        print(f'{payload}')
        r = requests.post(saf_url, headers=headers, json=payload)
        return r.json()
