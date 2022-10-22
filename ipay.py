#!/usr/bin/python3
import requests
import hmac
import hashlib
import json
import time as t
import csv
from sys import argv
with open("reversebotdata.csv", "a") as f:
    writer = csv.writer(f)
    #Needed to initate the payment request
    iPayTransact = "https://apis.ipayafrica.com/payments/v2/transact"

    #Triggers the SIM ToolKit for authorization of payment on the user's handset.
    iPayMpesa = "https://apis.ipayafrica.com/payments/v2/transact/push/mpesa"
    iPayAirtel = "https://apis.ipayafrica.com/payments/v2/transact/push/airtel"

    iPayKey = "SECretKey"  #use "demoCHANGED" for testing where vid is set to "demo"

    #Vendor ID
    iPayVid = "demo"  #Production Vendor ID will be provided once they have set up your Merchant account
    iPaySecret = b"demoCHANGED"
    order_id=1
    amount = argv[1]
    #print("Enter amount you want to donate: \n")
    phone = argv[2]
    #print("Enter you phone number: format 254xxxxxxxxx \n")
    #email=input("Enter your email? \n")
    email='ngangasammie@gmail.com'
    notifications=1
    send_receipt=0
    iPayData = {
        "live": 0,
        "oid": order_id,
        "inv": order_id,
        "amount": amount,
        "tel": phone,
        "eml": email,
        "vid": iPayVid,
        "curr": "KES",
        "p1": "YOUR-CUSTOM-PARAMETER",
        "p2": "YOUR-CUSTOM-PARAMETER",
        "p3": "YOUR-CUSTOM-PARAMETER",
        "p4": "YOUR-CUSTOM-PARAMETER",
        "cbk": "https://enktpf6b4e4rm.x.pipedream.net",
        "cst": notifications,
        "crl": 0,
        "autopay": 1
    }
    # The hash digital signature hash of the data for verification.
    hashCode = f"{iPayData['live']}{iPayData['oid']}{iPayData['inv']}{iPayData['amount']}{iPayData['tel']}{iPayData['eml']}{iPayData['vid']}{iPayData['curr']}{iPayData['p1']}{iPayData['p2']}{iPayData['p3']}{iPayData['p4']}{iPayData['cst']}{iPayData['cbk']}"
    h = hmac.new(iPaySecret, bytes(hashCode, 'utf-8'), hashlib.sha256)
    hash = h.hexdigest()
    iPayData["hash"] = hash

    data = iPayData
    response = requests.post(iPayTransact, headers={
                                "Content-Type": "application/json; "}, data=json.dumps(data))
    response = response.json()
    # print(response)
    response['data']['vid'] = data["vid"]
    response['data']['tel'] = phone
    response['data']['email'] = email


    stk_data = response
    outcome=stk_data['status']
    if outcome==1:
        tel=stk_data['data']['tel']
        vid = stk_data['data']['vid']
        sid = stk_data['data']['sid']
        order_id=stk_data['data']['oid']
        
        hashCode = f"{tel}{vid}{sid}"
        h = hmac.new(iPaySecret, bytes(hashCode, 'utf-8'), hashlib.sha256)
        hash = h.hexdigest()
        data = {
            "phone": tel,
            "vid": vid,
            "sid": sid,
            "hash": hash
        }
        response = requests.post(iPayMpesa, headers={
                                "Content-Type": "application/json; "}, data=json.dumps(data))
        response = response.json()
        if response['status'] == 1:
            print(True, "Successfully sent to the client", order_id)
        else:
            print(False, "An error occurred ")
        
    else:
        print(False, "An error occured while initiating request") 

    hashCode = f"{order_id}{iPayVid}"
    h = hmac.new(iPaySecret, bytes(hashCode, 'utf-8'), hashlib.sha256)
    hash = h.hexdigest()
    data = {
        "oid": order_id,
        "vid": vid,
        "hash": hash
    }

    # response = requests.post(iPayTransact, headers={
    #                             "Content-Type": "application/json; "}, data=json.dumps(data))
    # response = response.json()
    # if response['header_status'] == 200:
    #     print(True, response['data'])
    #     writer.writerow(response)
    # else:
    #     print(False, "Transaction not found or something went wrong")
    #     writer.writerow(response)
        