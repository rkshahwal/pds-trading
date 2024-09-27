import mysql.connector
import requests
import random
import json
from datetime import datetime
import os

# Establish a database connection
conn = mysql.connector.connect(
    host=os.getenv('servername'),
    user=os.getenv('username'),
    password=os.getenv('password'),
    database=os.getenv('dbname')
)

user = os.getenv('user')
input_amount = os.getenv('am')

order_id = "FSPD" + str(random.randint(10000, 999999))
date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

server_name = os.getenv('SERVER_NAME')
callback_url = 'https://fastwins.pro/trova/src/api/verify.php'
notify_url = callback_url
params = f"amount={input_amount}&callBackUrl=https://fastwins.pro/payment/verify.php&mchId=3a614346&notifyUrl=https://fastwins.pro/payment/verify.php&orderNo={order_id}&passageId=17701&key=2b5e7622cfcf42f8877f5e73198120d2"

md5_sign = hashlib.md5(params.encode()).hexdigest()

payload = {
    "amount": input_amount,
    "callBackUrl": "https://fastwins.pro/payment/verify.php",
    "mchId": "3a614346",
    "notifyUrl": "https://fastwins.pro/payment/verify.php",
    "orderNo": order_id,
    "passageId": "17701",
    "sign": md5_sign
}

response = requests.post('https://apis.wepayplus.com/client/collect/create', json=payload)

response_data = response.json()

if response_data.get('success') and 'payUrl' in response_data['data']:
    sql1 = "INSERT INTO recharge (username, recharge, status, upi, utr, rand) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (user, input_amount, 'unpaid', '0', '0', order_id)

    cursor = conn.cursor()
    cursor.execute(sql1, values)
    conn.commit()

    if cursor.rowcount == 1:
        print(f"Location: {response_data['data']['payUrl']}")
    else:
        print("Error description: " + cursor.statement)

    cursor.close()
    conn.close()
    exit()
else:
    print("Payment request failed. Please try again Or Wrong Details.")

