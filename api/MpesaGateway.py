import urllib
import json
from django.conf import settings
from mpesapy import Mpesa
import requests
from .auth import MpesaBase


class MpesaGatewayException(Exception):
    pass


class MpesaGateway:
    def __init__(self, access_token):
        self.apiKey_ = apiKey_
        self.B2BURLString = "https://sandbox.safaricom.co.ke/mpesa/b2b/v1/paymentrequest"
        self.B2CURLString = "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"
        self.C2BURLString = "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"

        self.initiator = "600384"
        self.securityCredential = "2222"
        self.CommandID = "MerchantToMerchantTransfer"
        self.senderIdentifierType = "4"
        self.recieverIdentifierType = "4"
        self.partyA = "600000"
        self.remarks = "remarks"
        self.queueTimeOutURL = "http://xx.218.132.xx:8080/transact/mpesa/api/dummylistener"
        self.ResultURL = "http://xx.218.132.xx:8080/transact/mpesa/api/dummylistener"
        self.Occasion = "ocassion"

        self.headers = {'Accept': 'application/json',
            'Authorization': f'Bearer {generateAccessToken()}'}

        self.HTTP_RESPONSE_OK = 200
        self.HTTP_RESPONSE_CREATED = 201

        # Turn this on if you run into problems. It will print the raw HTTP response from our server
        self.Debug = True


    def generateAccessToken():
        consumer_key = "DAoLQHjxGh3ks5mXXGqCuQtFAM7MYVvE"
        consumer_secret = "0SWNFJFAJAYCBktQ"
        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        print (r.text)

        return r.text


  
    def initiateB2BTransaction(self, recipient,  amount, accountReference):

        request = {'Initiator': self.initiator,
                    'SecurityCredential': self.securityCredential,
                    'CommandID': self.CommandID,
                    'Amount': amount,
                    'SenderIdentifierType': self.senderIdentifierType,
                    'RecieverIdentifierType': self.recieverIdentifierType,
                    'PartyA': self.partyA,
                    'PartyB': recipient,
                    'AccountReference': accountReference,
                    'Remarks': self.remarks,
                    'QueueTimeOutURL': self.queueTimeOutURL,
                    'ResultURL': self.ResultURL,
                    'Occasion': self.Occasion,
                      }
        print("send request")
        response = requests.post(self.B2BURLString, json=request, headers=self.headers).json()
        print(response)
        return response

        raise MpesaGatewayException(response)
