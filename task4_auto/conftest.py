import allure
import pytest
from selenium import webdriver
from main_ui import CartUI
from main_api import CartApi


# Фикстуры UI
@pytest.fixture(scope="session")
def driver():
    """Фикстура для веб-драйвера"""
    with allure.step("Открыть и настроить браузер"):
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.implicitly_wait(4)
        yield driver
        driver.quit()


@pytest.fixture()
def open_main_page(driver):
    """Фикстура для открытия главной страницы Алтайвита"""
    driver.get("https://altaivita.ru/")
    yield


@pytest.fixture()
def cart_ui(driver, open_main_page):
    """Фикстура для экземпляра CartUI"""
    return CartUI(driver)


# Фикстуры Api
@pytest.fixture
def cart_api():
    return CartApi()
