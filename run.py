import os

import eel

from common.api import ExecuteApi
from common.desktop import start

# import sys


app_name = "web"
end_point = "index.html"
size = (600, 700)


WRITE_CSV_PATH = os.path.join(os.getcwd(), "csv/search_{keyword}_{datetime}.csv")


@eel.expose
def fetch_data(shop_id: str) -> None:
    my_api = ExecuteApi(shop_id=shop_id)
    my_api.execute_api()


if __name__ == "__main__":
    start(app_name, end_point, size)
