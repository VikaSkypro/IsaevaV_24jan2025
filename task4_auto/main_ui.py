from typing import Dict, List, Tuple, Any, Optional
import allure
import pytest
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException
)


class CartUI:
    """Класс содержит описание UI методов для работы с товарами в корзине"""

    def __init__(self, driver):
        self.driver = driver

    def search_for_product(self, prod_name: Any) -> None:
        """Метод находит поле поиска, вводит фразу и нажимает Enter."""
        try:
            with allure.step("Ожидание появления поля поиска"):
                search_input = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, 'input[placeholder="Поиск товаров"]')
                    )
                )

            with allure.step("Ожидание, пока поле поиска станет доступным"):
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, 'input[placeholder="Поиск товаров"]')
                    )
                )

            with allure.step("Ввод фразы в поле поиска"):
                search_input.clear()
                search_input.send_keys(prod_name)
                search_input.send_keys(Keys.RETURN)

        except TimeoutException:
            print("Поле поиска не появилось в течение заданного времени.")
        except NoSuchElementException:
            print("Поле поиска не найдено.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


    def find_product(self, prod_name: Any) -> tuple[Any, Any] | tuple[None, None]:
        """Метод ищет нужный товар в результатах поиска
        и возвращает название и цену товара, если найден."""
        product_containers = self.driver.find_elements(
            By.XPATH, "/html/body/div[1]/main/div/div[4]/div[1]/div"
        )

        for container in product_containers:
            try:
                with allure.step("Получаем название товара"):
                    product_title = container.find_element(
                        By.XPATH, ".//div/div[2]/div/div/div[2]/a/span"
                    ).text

                if product_title == prod_name:
                    with allure.step("Получаем цену товара"):
                        product_price = container.find_element(
                            By.XPATH,
                            "/html/body/div[1]/main/div/div[4]/div[1]/div[1]/div/div[2]/div/div/div[4]/div[2]/div[2]/div/div[1]/span",
                        ).text
                    # print(f"Товар '{prod_name}' найден с ценой {product_price}.")
                    return product_title, product_price
            except NoSuchElementException:
                continue

        print(f"Товар '{prod_name}' не найден.")
        return None, None  # Возвращаем None, если товар не найден

    def add_product_to_cart(self, prod_name: Any) -> None:
        """Метод добавляет найденный товар в корзину."""
        product_title, product_price = self.find_product(prod_name)
        if product_title is not None:
            try:
                with allure.step("Добавляем товар в корзину"):
                    # Снова находим контейнер для товара
                    # Добавляем ожидание, чтобы убедиться, что контейнеры загружены
                    product_containers = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_all_elements_located(
                            (By.XPATH, "/html/body/div[1]/main/div/div[4]/div[1]/div")
                        )
                    )
                    for container in product_containers:
                        product_title_check = container.find_element(
                            By.XPATH, ".//div/div[2]/div/div/div[2]/a/span"
                        ).text
                        if product_title_check == product_title:
                            # Добавляем ожидание для кнопки добавления
                            add_button = WebDriverWait(container, 10).until(
                                EC.element_to_be_clickable(
                                    (By.XPATH, ".//div/div[4]/div/div[2]/div[1]/button")
                                )
                            )
                            add_button.click()
                            print(f"Товар '{prod_name}' добавлен в корзину.")
                            return
            except NoSuchElementException:
                print(f"Не удалось найти кнопку для добавления товара '{prod_name}'.")
        else:
            print(
                f"Не удалось добавить товар '{prod_name}' в корзину, так как он не найден."
            )

    def go_to_cart(self) -> None:
        """Метод перехода в корзину"""
        try:
            with allure.step("Нажимаем на кнопку предпросмотра корзины"):
                preview_cart_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (
                            By.CSS_SELECTOR,
                            "body > header > div.container > div.header__top > div.header__right > div.header__basket.js-basket-wrapper > a",
                        )
                    )
                )
                preview_cart_button.click()

            with allure.step('Нажимаем на кнопку "Перейти в корзину"'):
                go_to_cart_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (
                            By.CSS_SELECTOR,
                            "body > header > div.container > div.header__top > div.header__right > div.header__basket.js-basket-wrapper > div > div.dropdown-top.dropdown-padding > a",
                        )
                    )
                )
                go_to_cart_button.click()
                # print("Перешли в корзину.")
        except TimeoutException:
            print("Не удалось найти кнопку для перехода в корзину.")

    def get_cart_product_name(self) -> str | None:
        """Метод находит названия товаров в корзине"""
        try:
            cart_product_name = (
                WebDriverWait(self.driver, 10)
                .until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, ".basket__name"))
                )
                .text
            )
            return cart_product_name
        except TimeoutException:
            print("Не удалось получить название товара из корзины.")
            return None

    def get_cart_product_price(self) -> str | None:
        """Метод находит цены товаров в корзине"""
        try:
            cart_product_price = (
                WebDriverWait(self.driver, 10)
                .until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//span[@class='js-item-total']")
                    )
                )
                .text
            )
            return cart_product_price
        except TimeoutException:
            print("Не удалось получить цену товара из корзины.")
            return None

    def is_cart_empty(self):
        """Проверяем, есть ли товары в корзине"""
        cart_items = self.driver.find_elements(
            By.CSS_SELECTOR, ".basket__item.js-cart-item"
        )
        return len(cart_items) == 0

    def remove_all_products_from_cart(self):
        """Удаляет все товары из корзины"""
        with allure.step("Находим все товары в корзине"):
            cart_items = self.driver.find_elements(
                By.CSS_SELECTOR, ".basket__item.js-cart-item"
            )

        if not cart_items:
            print("Корзина пуста, нет товаров для удаления.")
            return

        with allure.step("Находим все кнопки удаления товаров"):
            remove_buttons = self.driver.find_elements(
                By.CSS_SELECTOR, ".basket__delete.js-item-delete"
            )

        with allure.step("Проходим по всем кнопкам и нажимаем на каждую"):
            for button in remove_buttons:
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(button))
                button.click()
                WebDriverWait(self.driver, 10).until(EC.staleness_of(button))
        print("Все товары из корзины были удалены.")
