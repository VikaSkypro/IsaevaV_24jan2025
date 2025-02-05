import allure
import pytest
from allure_commons.types import Severity
from main_api import CartApi


@allure.epic("API. Интернет-магазин Алтайвита")
@allure.feature("API. Тестирование корзины")
class TestCartApi:

    @allure.title("Тест: Добавление товаров в корзину")
    @allure.severity(Severity.BLOCKER)
    def test_add_prod_to_cart(self, cart_api):
        """Добавление товара в корзину.
        1. Добавляем нужный товар в корзину.
        2. Удаляем все товары для чистоты корзины."""
        product_id = 6939  # id товара
        expected_price = 649  # Ожидаемая цена товара

        with allure.step("Для теста удаляем все из корзины, если не пусто"):
            cart_api.removing_items_cart(product_id=product_id)

        response, status_code = cart_api.add_prod_to_cart(product_id=product_id)
        print("Добавление в корзину:")
        for key, value in response.items():
            print(f"{key}: {value}")
        with allure.step("Проверяем, что статус код 200"):
            assert status_code == 200, f"Ожидался статус код 200, получен {status_code}"

        with allure.step("Проверяем, что цена товара равна ожидаемой"):
            assert (
                response.get("products_amount") == expected_price
            ), f"Ожидалась цена {expected_price}, получена {response.get('products_amount')}"

        with allure.step("Удаляем продукт из корзины, чтобы очистить её после теста"):
            remove_response, remove_status_code = cart_api.removing_items_cart(
                product_id=product_id
            )
            print("Очистка корзины:")
            for key, value in remove_response.items():
                print(f"{key}: {value}")
            with allure.step("Проверяем, что статус код 200"):
                assert (
                    remove_status_code == 200
                ), f"Ожидался статус код 200 при удалении, получен {remove_status_code}"

    @allure.title("Тест: Получение списка товаров в корзине")
    @allure.severity(Severity.BLOCKER)
    def test_get_cart_content(self, cart_api):
        """Просмотр содержимого корзины.
        1. Добавляем нужный товар в корзину.
        2. Проверяем содержимое корзины.
        3. Удаляем все товары для чистоты корзины."""
        LANG_key = "ru"
        S_cur_code = "rub"
        product_id = 6939  # ID продукта, который будем добавлять

        with allure.step("Для теста удаляем все из корзины, если не пусто"):
            cart_api.removing_items_cart(product_id=product_id)

        with allure.step("Добавляем продукт в корзину для теста"):
            add_response, add_status_code = cart_api.add_prod_to_cart(
                product_id=product_id
            )
            print("Add Response:")
            print(add_response)
            with allure.step("Проверяем, что статус код 200"):
                assert (
                    add_status_code == 200
                ), f"Ожидался статус код 200 при добавлении, получен {add_status_code}"

        with allure.step("Получаем содержимое корзины"):
            response, status_code = cart_api.get_cart_content(LANG_key, S_cur_code)
            print("Response:")
            print(response)  # Вывод HTML-содержимого корзины
            with allure.step("Проверяем, что статус код 200"):
                assert (
                    status_code == 200
                ), f"Ожидался статус код 200, получен {status_code}"

            with allure.step(
                "Проверяем, что продукт с нужным ID присутствует в содержимом корзины"
            ):
                assert (
                    f'data-item-product-id="{product_id}"' in response
                ), f"Продукт с ID {product_id} не найден в содержимом корзины"

        with allure.step("Удаляем продукт из корзины, чтобы очистить её после теста"):
            remove_response, remove_status_code = cart_api.removing_items_cart(
                product_id=product_id
            )
            print("Remove Response:")
            print(remove_response)
            with allure.step("Проверяем, что статус код 200"):
                assert (
                    remove_status_code == 200
                ), f"Ожидался статус код 200 при удалении, получен {remove_status_code}"

    @allure.title("Тест: Удаление товара из корзины")
    @allure.severity(Severity.BLOCKER)
    def test_remove_product_from_cart(self, cart_api):
        """Тест на удаление товара из корзины.
        1. Добавляем товар в корзину.
        2. Удаляем товар из корзины.
        3. Проверяем, что товар был удален."""

        LANG_key = "ru"
        S_cur_code = "rub"
        product_id = 6939  # ID продукта, который будем добавлять

        with allure.step("Для теста удаляем все из корзины, если не пусто"):
            cart_api.removing_items_cart(product_id=product_id)

        with allure.step("Добавляем продукт в корзину для теста"):
            add_response, add_status_code = cart_api.add_prod_to_cart(
                product_id=product_id
            )
            print("Add Response:")
            print(add_response)
            with allure.step("Проверяем, что статус код 200"):
                assert (
                    add_status_code == 200
                ), f"Ожидался статус код 200 при добавлении, получен {add_status_code}"
            with allure.step("Сохраняем цену добавленного товара"):
                products_amount = str(add_response["products_amount"])

        with allure.step("Удаляем продукт из корзины"):
            remove_response, remove_status_code = cart_api.removing_items_cart(
                product_id=product_id
            )
            print("Remove Response:")
            print(remove_response)
            with allure.step("Проверяем, что статус код 200"):
                assert (
                    remove_status_code == 200
                ), f"Ожидался статус код 200 при удалении, получен {remove_status_code}"
            with allure.step(
                "Проверяем, что цена удаляемого товара равна цене добавленного товара"
            ):
                price_to_delete = remove_response["price_to_delete"]
                assert (
                    price_to_delete == products_amount
                ), f"Цена удаляемого товара {price_to_delete} не равна цене добавленного товара {products_amount}"

        with allure.step("Проверяем, что продукт был удален из корзины"):
            response, status_code = cart_api.get_cart_content(LANG_key, S_cur_code)
            print("Response:")
            print(response)  # Вывод HTML-содержимого корзины
            with allure.step("Проверяем, что статус код 200"):
                assert (
                    status_code == 200
                ), f"Ожидался статус код 200, получен {status_code}"

            with allure.step(
                "Проверяем, что продукт с нужным ID отсутствует в содержимом корзины"
            ):
                assert (
                    f'data-item-product-id="{product_id}"' not in response
                ), f"Продукт с ID {product_id} все еще присутствует в содержимом корзины"
