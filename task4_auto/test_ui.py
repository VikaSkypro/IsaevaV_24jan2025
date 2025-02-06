import allure
import pytest
from allure_commons.types import Severity
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException)
from main_ui import CartUI
from time import sleep


@allure.epic("UI. Интернет-магазин Алтайвита")
@allure.feature("UI. Тестирование корзины")
class TestCartUi:

    @allure.title("Тест: Добавление товара в корзину")
    @allure.severity(Severity.BLOCKER)
    def test_ui_search_and_add_product(self, cart_ui):
        """Тест выполняет поиск товара по полному названию,
        добавляет его в корзину и сравнивает название и цену"""
        with allure.step("Ввод полного названия товара и поиск"):
            prod_name = "Алтайский ключ, 30 капсул по 500 мг. Набор из 6 шт"
            cart_ui.search_for_product(prod_name)
            sleep(3)  # Добавлены для наглядности выполнения теста
        with allure.step("Поиск товара в результатах поиска"):
            product_title, product_price = cart_ui.find_product(prod_name)
            # sleep(2)  # Добавлены для наглядности выполнения теста
        with allure.step("Добавление товара в корзину"):
            cart_ui.add_product_to_cart(prod_name)
            # sleep(2)  # Добавлены для наглядности выполнения теста
        with allure.step("Переход в корзину"):
            cart_ui.go_to_cart()
            # sleep(3)  # Добавлены для наглядности выполнения теста
        with allure.step("Проверка названия товара с ожидаемым"):
            cart_product_name = cart_ui.get_cart_product_name()
            assert (
                cart_product_name == prod_name
            ), f"Ошибка: в корзине находится товар '{cart_product_name}', ожидался '{prod_name}'."
            print(f"Товар '{prod_name}' успешно найден в корзине.")
        with allure.step("Проверка цены товара с ожидаемой"):
            cart_product_price = cart_ui.get_cart_product_price()
            with allure.step("Нормализуем цены перед сравнением (приводим к одному виду)"):
                normalized_cart_product_price = cart_product_price.replace(" ", "").replace(
                    "₽", ""
                )
                normalized_product_price = product_price.replace(" ", "").replace("₽", "")
                print(
                    f"Цена добавляемого продукта: {product_price}, Цена в корзине: {cart_product_price}"
                )
                assert (
                    normalized_cart_product_price == normalized_product_price
                ), f"Ошибка: цена товара '{cart_product_price}', ожидалась '{product_price}'"
        with allure.step("Удаление товара после теста"):
            cart_ui.remove_all_products_from_cart()

    @allure.title("Тест: Удаление товаров из корзины")
    @allure.severity(Severity.BLOCKER)
    def test_ui_delete_product_to_cart(self, cart_ui):
        """Тест выполняет удаление добавленных в корзину товаров"""
        with allure.step("Ввод полного названия товара и поиск"):
            prod_name = "Ежовик с гинкго билоба 30 капсул по 500 мг, Алфит"
            cart_ui.search_for_product(prod_name)
        with allure.step("Поиск товара в результатах поиска"):
            cart_ui.find_product(prod_name)
        with allure.step("Добавление товара в корзину"):
            cart_ui.add_product_to_cart(prod_name)
        with allure.step("Переход в корзину"):
            cart_ui.go_to_cart()
            # sleep(2) # Добавлены для наглядности выполнения теста
        with allure.step("Удаление товара"):
            cart_ui.remove_all_products_from_cart()
            assert cart_ui.is_cart_empty(), "Корзина не пуста, товары не были удалены."
            # sleep(3)  # Добавлены для наглядности выполнения теста
