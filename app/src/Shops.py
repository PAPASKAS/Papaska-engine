from typing import Type
from selenium.common import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class Shop:
    @staticmethod
    def get_value(telephone: WebElement, css_selector: str, timeout: int = 15) -> str or None:
        try:
            return WebDriverWait(telephone, timeout=timeout).until(
                expected_conditions.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            ).text
        except NoSuchElementException:
            return None
        except StaleElementReferenceException:
            return None
        except TimeoutException:
            return None

    @staticmethod
    def get_price(price: str) -> int:
        return int(''.join(x for x in price if x.isdigit()))

    @staticmethod
    def get_name(name: str) -> str:
        if name.partition('GB')[1] != '':
            return ''.join(name.partition('GB')[:2])
        elif name.partition('TB')[1] != '':
            return ''.join(name.partition('TB')[:2])
        elif name.partition('ГБ')[1] != '':
            return ''.join(name.partition('ГБ')[:2])
        elif name.partition('ТБ')[1] != '':
            return ''.join(name.partition('ТБ')[:2])
        elif name.partition('[')[1] != '':
            return ''.join(name.partition('[')[:1])
        elif name.partition('(')[1] != '':
            return ''.join(name.partition('(')[:1])
        else:
            return name

    @staticmethod
    def get_data(
        telephone: WebElement,
        name_css_selector, current_price_css_selector, before_discount_css_selector,
    ) -> dict[str, Type[str | int | None]]:
        return {
            'name': Shop.get_value(telephone, name_css_selector),
            'current_price': Shop.get_value(telephone, current_price_css_selector),
            'before_discount': Shop.get_value(telephone, before_discount_css_selector, 1),
        }


class Dns:
    @staticmethod
    def get_phone(telephone: WebElement) -> dict[str, Type[str | int | None]]:
        data = Shop.get_data(telephone, 'a.catalog-product__name', 'div.product-buy__price', 'span.product-buy__prev')

        if data['name'] is None or data['current_price'] is None:
            return data
        else:
            return {
                'name': ' '.join(Shop.get_name(data['name']).split()[1:]),
                'current_price': Shop.get_price(data['current_price'].partition('₽')[0]),
                'before_discount': None if data['before_discount'] is None else Shop.get_price(data['before_discount']),
            }

    @staticmethod
    def get_cellular_phone(telephone: WebElement) -> dict[str, Type[str | int | None]]:
        data = Shop.get_data(telephone, 'a.catalog-product__name', 'div.product-buy__price', 'span.product-buy__prev')

        if data['name'] is None or data['current_price'] is None:
            return data
        else:
            return {
                'name': ' '.join(Shop.get_name(data['name']).split()[:-1]),
                'current_price': Shop.get_price(data['current_price'].partition('₽')[0]),
                'before_discount': None if data['before_discount'] is None else Shop.get_price(data['before_discount']),
            }

    @staticmethod
    def find_need_page(driver: webdriver, phone_type: str) -> None:
        if phone_type == 'smartphones':
            driver.get('https://www.dns-shop.ru/catalog/17a8a01d16404e77/smartfony/')
        elif phone_type == 'cellular_phones':
            driver.get('https://www.dns-shop.ru/catalog/17a89fea16404e77/sotovye-telefony/')
        elif phone_type == 'tablet':
            driver.get('https://www.dns-shop.ru/catalog/17a8a05316404e77/planshety/')


class Svyaznoy:
    @staticmethod
    def find_need_page(driver: webdriver, phone_type: str) -> None:
        if phone_type == 'smartphones':
            driver.get('https://www.svyaznoy.ru/catalog/phone/224')
        elif phone_type == 'tablet':
            driver.get('https://www.svyaznoy.ru/catalog/notebook/7063')

    @staticmethod
    def get_phone(telephone: WebElement):
        data = Shop.get_data(telephone, 'span.b-product-block__name', 'span.b-product-block__visible-price', 's.b-product-block__price-old')

        if data['name'] is None or data['current_price'] is None:
            return data
        else:
            return {
                'name': Shop.get_name(data['name']),
                'current_price': Shop.get_price(data['current_price'].partition('₽')[0]),
                'before_discount': None if data['before_discount'] is None else Shop.get_price(data['before_discount']),
            }


class MVideo:
    @staticmethod
    def find_need_page(driver: webdriver, phone_type: str) -> None:
        if phone_type == 'smartphones':
            driver.get('https://www.mvideo.ru/smartfony-i-svyaz-10/smartfony-205/')
        elif phone_type == 'cellular_phones':
            driver.get('https://www.mvideo.ru/smartfony-i-svyaz-10/mobilnye-telefony-95')
        elif phone_type == 'tablet':
            driver.get('https://www.mvideo.ru/noutbuki-planshety-komputery-8/planshety-195')

    @staticmethod
    def get_phone(telephone: WebElement):
        data = Shop.get_data(telephone, 'a.product-title__text', 'span.price__main-value', 'span.price__sale-value')

        if data['name'] is None or data['current_price'] is None:
            return data
        else:
            return {
                'name': Shop.get_name(data['name']),
                'current_price': Shop.get_price(data['current_price'].partition('₽')[0]),
                'before_discount': None if data['before_discount'] is None else Shop.get_price(data['before_discount']),
            }


class BQ:
    @staticmethod
    def find_need_page(driver: webdriver, phone_type: str) -> None:
        if phone_type == 'smartphones':
            driver.get('https://bq.ru/catalog/smartfony/vse-smartfony/')
        elif phone_type == 'cellular_phones':
            driver.get('https://bq.ru/catalog/planshety/')
        elif phone_type == 'tablet':
            driver.get('https://bq.ru/catalog/telefony/')

    @staticmethod
    def get_phone(telephone: WebElement):
        data = Shop.get_data(telephone, 'div.name', 'div.price', 'div.category')  # [3] no such element

        if data['name'] is None or data['current_price'] is None:
            return data
        else:
            return {
                'name': Shop.get_name(data['name']),
                'current_price': Shop.get_price(data['current_price'].partition('₽')[0]),
                'before_discount': None,
            }
