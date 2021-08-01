# import codecs
# import csv
# import math
# import random
import math
import re
import sys
from time import sleep

import requests

PURPLE = "\033[35m"
RED = "\033[31m"
CYAN = "\033[36m"
OKBLUE = "\033[94m"
OKGREEN = "\033[92m"
WARNING = "\033[93m"
FAIL = "\033[91m"
ENDC = "\033[0m"

args = sys.argv
# shopName = args[1]
counter = 0
url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"
payload = {
    "applicationId": 1019079537947262807,
    "hits": 30,
    "shopCode": "f433641-gyokuto",
    "page": 1,
}
r = requests.get(url, params=payload)
resp = r.json()
print("【num of item】", resp["count"])
total = int(resp["count"])
Max = math.ceil(total / 30)
print("【total page】", Max)

if Max > 100:
    Max = 100
    print("100ページ（3000アイテム）を超えています．")
    print("カテゴリ別に回すことを勧めます.")
    sleep(3)
print("-" * 40)
sleep(1)

for i in range(1, int(Max) + 1):
    url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"
    payload = {
        "applicationId": 1019079537947262807,
        "hits": 30,
        "shopCode": "f433641-gyokuto",
        "page": i,
    }
    r = requests.get(url, params=payload)
    resp = r.json()
    for i in resp["Items"]:
        counter = counter + 1
        print("【No.】" + PURPLE + str(counter) + ENDC)
        item = i["Item"]
        name = item["itemName"]
        if len(name) >= 30:
            print("【Name】" + OKGREEN + str(name[:30].encode("utf-8")) + "..." + ENDC)
        else:
            print("【Name】" + OKGREEN + str(item["itemName"].encode("utf-8")) + ENDC)
        print("【Price】" + CYAN + "¥" + str(item["itemPrice"]) + ENDC)

        # ポイント分（自分の場合は最低４倍）を差し引く
        price = int(item["itemPrice"] * 0.96)
        print("【URL】", item["itemUrl"])
        URL = item["itemUrl"]
        print("【shop】", item["shopName"])
        text = item["itemCaption"]

        JAN = ""
        postCode_0 = re.findall("[0-9]{13}", URL)
        if len(postCode_0) == 1:
            JAN = postCode_0[0]
            print("【JAN】" + OKGREEN + str(JAN) + ENDC)
        else:
            postCode = re.findall("[0-9]{13}", text)
            len_postCode = len(postCode)
            if len_postCode == 1:
                JAN = postCode[0]
                print("【JAN】" + WARNING + str(postCode[0]) + ENDC)
            # a.write(str(JAN)+','+str(name.encode('utf-8'))+','+str(price)+','+str(URL)+'\n')
            else:
                JAN = "NONE"
                print("【JAN】" + WARNING + "JAN: NONE" + ENDC)
        print("")
        sleep(0.1)
# a.close()
