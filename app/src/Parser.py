from typing import Callable, Type
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from app.models import Phones
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from .Shops import Dns, Svyaznoy, MVideo, BQ


class Parser:
    driver: webdriver

    def __init__(self) -> None:
        chrome_options: Options = webdriver.ChromeOptions()
        chrome_options.add_argument('disable-gpu')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_experimental_option('prefs', {
            'profile.managed_default_content_settings.images': 2,
            'profile.managed_default_content_settings.stylesheets': 2,
            'profile.managed_default_content_settings.media_stream': 2,
            'profile.managed_default_content_settings.mixed_script': 2,
            'plugins': 2,
            'notification': 2,
            'geolocation': 2,
            'automatic_downloads': 2
        })

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            chrome_options=chrome_options
        )
        stealth(
            driver=self.driver,
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36',
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

        try:
            types_phones: list[str] = ['smartphones', 'tablet', 'cellular_phones']

            # svyaznoy
            for phone_type in types_phones[:2]:
                self.__main(
                    shop='svyaznoy', btn_to_next_page='li.next a',
                    phones='div.b-product-block',
                    find_need_page=Svyaznoy.find_need_page,
                    type_phones=phone_type,
                    get_phone=Svyaznoy.get_phone,
                )

            # mVideo
            for type_phone in types_phones:
                self.__main(
                    shop='mVideo', btn_to_next_page='a.page-link.icon.ng-star-inserted',
                    phones='div.product-cards-layout__item.ng-star-inserted',
                    find_need_page=MVideo.find_need_page,
                    type_phones=type_phone,
                    get_phone=MVideo.get_phone,
                )

            #  DNS
            for type_phone in types_phones[:2]:
                self.__main(
                    shop='dns',
                    btn_to_next_page='.pagination-widget__page-link.pagination-widget__page-link_next',
                    phones='div.catalog-product.ui-button-widget',
                    type_phones=type_phone,
                    find_need_page=Dns.find_need_page,
                    get_phone=Dns.get_phone,
                )

            self.__main(
                shop='dns',
                btn_to_next_page='.pagination-widget__page-link.pagination-widget__page-link_next',
                phones='div.catalog-product.ui-button-widget',
                type_phones=types_phones[2],
                find_need_page=Dns.find_need_page,
                get_phone=Dns.get_cellular_phone,
            )

            # BQ
            for type_phone in types_phones:
                self.__main(
                    shop='bq',
                    btn_to_next_page='.pagination-widget__page-link.pagination-widget__page-link',  # 1 page on this site
                    phones='div.col-xl-3.col-md-3.col-sm-6',
                    find_need_page=BQ.find_need_page,
                    type_phones=type_phone,
                    get_phone=BQ.get_phone,
                )
        finally:
            self.driver.close()

    def __main(
        self, shop: str, btn_to_next_page: str,
        phones: str, type_phones: str,
        find_need_page: Callable[[webdriver, str], None],
        get_phone: Callable[[WebElement], dict[str, Type[str | int | None]]],
    ) -> None:
        find_need_page(self.driver, type_phones)

        unique_name: set[str] = set()
        while True:
            try:
                ec = (NoSuchElementException, StaleElementReferenceException, TimeoutException)
                document: list[WebElement] = WebDriverWait(self.driver, timeout=10, ignored_exceptions=ec)\
                    .until(expected_conditions.visibility_of_all_elements_located((By.CSS_SELECTOR, phones)))
                for telephone in document:
                    self.driver.execute_script('arguments[0].scrollIntoView(true)', telephone)
                    phone = get_phone(telephone)

                    if phone['name'] is None or phone['current_price'] is None:
                        continue

                    if phone['name'] in unique_name:
                        continue

                    unique_name.add(phone['name'])
                    correct_phone = {
                        'shop': shop,
                        'name': phone['name'].strip(),
                        'name_lower': phone['name'].strip().lower(),
                        'current_price': phone['current_price'],
                        'before_discount': phone['before_discount'],
                    }

                    Phones.objects.update_or_create(
                        **correct_phone,
                        defaults=correct_phone,
                    )

                # to the next page
                element: WebElement = WebDriverWait(self.driver, timeout=10).until(
                    expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, btn_to_next_page))
                )
                if element.get_attribute('href') == 'javascript:':  # dns
                    raise NoSuchElementException()
                self.driver.execute_script('arguments[0].click();', element)
            except TimeoutException:  # mVideo last page
                break
            except NoSuchElementException:
                break
