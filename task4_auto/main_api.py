import requests
import allure
from typing import Dict, List, Tuple, Any, Optional
from requests import Response


class CartApi:
    """Класс содержит описание API методов для работы с товарами в корзине"""

    def __init__(self) -> None:
        self.base_url: str = "https://altaivita.ru/engine/cart/"
        self.CID: str = "702bf3e9607ccaa9a3c98f67811520b4"  # id Сессии корзины
        self.my_headers: Dict[str, str] = {
            "Cookie": f"CID={self.CID};",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    @allure.step("API. Добавление товара в корзину")
    def add_prod_to_cart(
        self,
        product_id: int = 6939,
        this_listId: str = "search_list",
        LANG_key: str = "ru",
        S_wh: str = "1",
        S_cur_code: str = "rub",
        S_koef: str = "1",
        quantity: int = 1,
    ) -> Tuple[Dict[str, Any], int]:
        """Добавляет товар в корзину"""
        payload: Dict[str, Any] = {
            "product_id": product_id,
            "this_listId": this_listId,
            "LANG_key": LANG_key,
            "S_wh": S_wh,
            "S_CID": self.CID,
            "S_cur_code": S_cur_code,
            "S_koef": S_koef,
            "quantity": quantity,
        }

        response: Response = requests.post(
            f"{self.base_url}add_products_to_cart_from_preview.php",
            headers=self.my_headers,
            data=payload,
        )

        response_json: Dict[str, Any] = response.json()  # Получаем JSON-ответ
        return response_json, response.status_code  # Возвращаем JSON и статус код

    @allure.step("API. Получение содержимого корзины")
    def get_cart_content(
        self, LANG_key: str = "ru", S_cur_code: str = "rub"
    ) -> Tuple[str, int]:
        """Получает содержимое корзины"""
        payload: Dict[str, str] = {
            "LANG_key": LANG_key,
            "S_CID": self.CID,
            "S_cur_code": S_cur_code,
        }

        response: Response = requests.get(
            f"{self.base_url}ajax_show_cart_preview.php",
            params=payload,
            headers=self.my_headers,
        )

        return response.text, response.status_code  # Возвращаем HTML и статус код

    @allure.step("API. Изменение количества товара в корзине")
    def increase_items_cart(
        self,
        item_id: str,
        quantity: int = 2,
        LANG_key: str = "ru",
        S_cur_code: str = "rub",
    ) -> Tuple[Dict[str, Any], int]:
        """Увеличивает количество товара в корзине"""
        payload: Dict[str, Any] = {
            "itemID": item_id,
            "quantity": quantity,
            "action": "update_quantity",
            "LANG_key": LANG_key,
            "S_wh": "1",
            "S_CID": self.CID,
            "S_cur_code": S_cur_code,
            "S_koef": "1",
        }

        response: Response = requests.post(
            f"{self.base_url}action_with_basket_on_cart_page.php",
            headers=self.my_headers,
            data=payload,
        )

        response_json: Dict[str, Any] = response.json()
        return response_json, response.status_code

    @allure.step("API. Удаление товаров из корзины")
    def removing_items_cart(
        self, product_id: int, LANG_key: str = "ru", S_cur_code: str = "rub"
    ) -> Tuple[Dict[str, Any], int]:
        """Удаление товаров из корзины"""
        payload: Dict[str, Any] = {
            "product_id": product_id,
            "LANG_key": LANG_key,
            "S_wh": "1",
            "S_CID": self.CID,
            "S_cur_code": S_cur_code,
        }

        response: Response = requests.post(
            f"{self.base_url}delete_products_from_cart_preview.php",
            headers=self.my_headers,
            data=payload,
        )

        response_json: Dict[str, Any] = response.json()
        return response_json, response.status_code
