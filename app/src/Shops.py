from typing import Type
from bs4 import PageElement
from selenium.common import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


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


def get_price(price: str) -> int | None:
    return int(''.join(x for x in price if x.isdigit()))


def get_name(name: str | None) -> str:
    if name.partition('GB')[1] != '':
        return ''.join(name.partition('GB')[:2])
    elif name.partition('TB')[1] != '':
        return ''.join(name.partition('TB')[:2])
    elif name.partition('ГБ')[1] != '':
        return ''.join(name.partition('ГБ')[:2])
    elif name.partition('ТБ')[1] != '':
        return ''.join(name.partition('ТБ')[:2])
    else:
        return ''.join(name.partition('(')[:1])


def get_data(
    telephone: WebElement,
    name_css_selector, current_price_css_selector, before_discount_css_selector,
) -> dict[str, Type[str | int | None]]:
    return {
        'name': get_value(telephone, name_css_selector),
        'current_price': get_value(telephone, current_price_css_selector),
        'before_discount': get_value(telephone, before_discount_css_selector, 1),
    }


class Dns:
    @staticmethod
    def get_phone(telephone: WebElement) -> dict[str, Type[str | int | None]]:
        data = get_data(
            telephone=telephone,
            name_css_selector='a.catalog-product__name',
            current_price_css_selector='div.product-buy__price',
            before_discount_css_selector='span.product-buy__prev'
        )

        if data['name'] is None or data['current_price'] is None:
            return data
        else:
            return {
                'name': ' '.join(get_name(data['name']).split()[1:]),
                'current_price': get_price(data['current_price'].partition('₽')[0]),
                'before_discount': None if data['before_discount'] is None else get_price(data['before_discount']),
            }

    @staticmethod
    def find_need_page(driver: webdriver, type: str) -> None:
        driver.get('https://www.dns-shop.ru/catalog/')
        driver.implicitly_wait(5)
        menu: WebElement = driver.find_elements(
            By.CSS_SELECTOR,
            'div.subcategory__item.subcategory__item_with-childs',
        )[1]
        menu.click()

        if type == 'smartphones' or type == 'cellular_phones':
            menu.find_elements(By.CSS_SELECTOR, 'li.subcategory__childs-list-item')[1].click()

            if type == 'smartphones':
                driver.find_elements(By.CSS_SELECTOR, 'a.subcategory__item.ui-link.ui-link_blue')[0].click()
            elif type == 'cellular_phones':
                driver.find_elements(By.CSS_SELECTOR, 'a.subcategory__item.ui-link.ui-link_blue')[3].click()
        elif type == 'tablet':
            menu.find_elements(By.CSS_SELECTOR, 'li.subcategory__childs-list-item')[2].click()
            driver.find_elements(By.CSS_SELECTOR, 'a.subcategory__item.ui-link.ui-link_blue')[0].click()


class Svyaznoy:
    @staticmethod
    def find_need_page(driver: webdriver) -> None:
        driver.get('https://www.svyaznoy.ru/catalog/phone/')

    @staticmethod
    def get_telephone(telephone: PageElement) -> dict[str, Type[str | int | None]]:
        data = {
            'name': str,
            'current_price': int,
            'before_discount': int | None,
        }

        name: str = telephone.find('span', class_='b-product-block__name').text
        if name.partition('GB')[1] != '':
            data['name'] = ' '.join(name.partition('GB')[:2])
        elif name.partition('TB')[1] != '':
            data['name'] = ' '.join(name.partition('TB')[:2])
        else:
            data['name'] = ' '.join(name.partition('(')[:1])

        data['current_price'] = get_price(telephone.find('span', class_='b-product-block__visible-price').text)

        try:
            data['before_discount'] = get_price(telephone.find('s', class_='b-product-block__price-old').text)
        except AttributeError:
            data['before_discount'] = None

        return data


class MVideo:
    @staticmethod
    def find_need_page(driver: webdriver):
        driver.get('https://www.mvideo.ru/telefony')
        driver.find_elements(By.CSS_SELECTOR, 'li.sidebar-category a')[0].click()

    @staticmethod
    def get_telephone(telephone: PageElement) -> dict[str, Type[str | int | None]] | None:
        data: dict[str, Type[str | int | None]] = {}

        # data['name']
        try:
            name: str = telephone.find('a', class_='product-title__text').text
            if name.partition('GB')[1] != '':
                data['name'] = ' '.join(name.partition('GB')[:2])
            elif name.partition('TB')[1] != '':
                data['name'] = ' '.join(name.partition('TB')[:2])
            else:
                data['name'] = ' '.join(name.partition('(')[:1])
        except AttributeError:
            return None

        # data['current_price']
        data['current_price'] = get_price(telephone.find('span', class_='price__main-value').text)

        # data['before_discount']
        try:
            data['before_discount'] = get_price(telephone.find('s', class_='price__sale-value').text)
        except AttributeError:
            data['before_discount'] = None

        return data


class BQ:
    @staticmethod
    def find_need_page(driver: webdriver):
        driver.get('https://bq.ru/catalog/smartfony/vse-smartfony/')
        # loading
        for i in range(10):
            driver.execute_script("document.querySelector('#loader').click()")

    @staticmethod
    def get_telephone(telephone: PageElement):
        return {
            'before_discount': None,
            'name': telephone.find('div', class_='name').text,
            'type': telephone.find('div', class_='name').text.split()[0],
            'current_price': get_price(telephone.find('div', class_='price').text),
        }
