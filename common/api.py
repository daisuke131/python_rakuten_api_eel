import json
import math
from concurrent.futures import ThreadPoolExecutor
from time import sleep

import eel
import requests

RAKUTEN_ITEM_SEARCH_URL = (
    "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"
)
APP_ID = "1019079537947262807"


class ExecuteApi:
    def __init__(self, shop_id: str) -> None:
        self.params = {}
        self.page_count: int
        self.data_count: int = 0
        # self.result: json
        self.set_params(shop_id)

    def set_params(self, shop_id: str) -> None:
        self.params = {
            "applicationId": APP_ID,
            "shopCode": shop_id,
            "format": "json",
        }

    # def fetch_page_count(self) -> None:
    #     res = requests.get(RAKUTEN_ITEM_SEARCH_URL, self.params)
    #     res = self.fetch_json()
    #     self.page_count = math.ceil(res["count"] / 30)

    # def fetch_json(self) -> json:
    #     res = requests.get(RAKUTEN_ITEM_SEARCH_URL, self.params)
    #     if not (300 > res.status_code >= 200):
    #         eel.alert_js("データを取得できませんでした。")
    #         return
    #     return res.json()

    def execute_api(self) -> bool:
        # ページ取得
        r = requests.get(RAKUTEN_ITEM_SEARCH_URL, self.params)
        if not (300 > r.status_code >= 200):
            eel.alert_js("データを取得できませんでした。")
            return
        res = r.json()
        if len(res) == 0:
            eel.alert_js("指定のショップコードのデータは０件です。")
            return
        self.page_count = math.ceil(res["count"] / 30)
        eel.output_oder_list("{}件抽出".format(res["count"]))
        # データ取得
        eel.output_oder_list("===========start===========")

        with ThreadPoolExecutor(max_workers=2) as executor:
            for i in range(self.page_count):
                self.params["page"] = i + 1
                executor.submit(self.fetch_data)
        eel.output_oder_list("===========end===========")

    def fetch_data(self):
        r = requests.get(RAKUTEN_ITEM_SEARCH_URL, self.params)
        res = r.json()
        self.output_api_data(res)

    def output_api_data(self, res: json) -> None:
        for item in res["Items"]:
            self.data_count += 1
            item_details = item["Item"]
            eel.output_oder_list(f"--------{self.data_count}品目--------")
            self.dawfdwafa(item_details, "itemCode")
            self.dawfdwafa(item_details, "itemName")
            self.dawfdwafa(item_details, "shopCode")
            self.dawfdwafa(item_details, "shopName")
            sleep(0.1)

    def dawfdwafa(self, item_details, code):
        try:
            eel.output_oder_list("【{}】: {}".format(code, item_details[code]))
        except Exception:
            eel.output_oder_list(f"【{code}】: 取得できませんでした。")
