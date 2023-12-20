import os
import re
import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from locators import *

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("--hide-scrollbars")
options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

baseURL = 'https://www.saucedemo.com/'
file_path = os.path.dirname(os.path.dirname(__file__))
filename = os.path.join(file_path, 'leapfrog_assessment/screenshots/')


class BaseLoginClass:
    def login(self, driver):
        driver.get(baseURL)
        wait = WebDriverWait(driver, 60)
        wait.until(EC.visibility_of_element_located((By.XPATH, check_page)))

        # Check if the user can log in into the page or not
        driver.find_element(By.ID, username).send_keys(username_value)
        driver.find_element(By.ID, password).send_keys(password_value)
        driver.find_element(By.ID, submit).click()

        try:
            element = driver.find_element(By.CLASS_NAME, product_page)
            assert element.is_displayed()
            print(f"Sign in Successful with username {username_value}")
        except NoSuchElementException as e:
            driver.save_screenshot(filename + 'sign_in_unsuccessful.png')
            raise Exception("Sign in Unsuccessful") from e


@pytest.fixture
def driver():
    driver_instance = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver_instance.maximize_window()
    yield driver_instance
    driver_instance.quit()


class TestSelenium(BaseLoginClass):

    def test_login_standard_user(self, driver):
        self.login(driver)

    def test_add_to_cart(self, driver):
        self.login(driver)
        # Check if the items can be added in the cart by a logged-in user or not
        driver.find_element(By.ID, add_to_cart).click()
        driver.find_element(By.ID, add_to_cart_1).click()
        check_cart = driver.find_element(By.CLASS_NAME, cart_value).text
        try:
            assert check_cart == "2"
            print("User can add items to cart")
            driver.save_screenshot(filename + 'add_to_cart.png')
        except NoSuchElementException as e:
            driver.save_screenshot(filename + 'add_to_cart_unsuccessful.png')
            raise Exception("User can't add items to cart") from e

    def test_ascending_order_name(self, driver):
        self.login(driver)
        # Find all item_name and check if they are sorted in ascending order or not
        items = driver.find_elements(By.CSS_SELECTOR, ".inventory_item_name")
        items_all = [item.text for item in items]
        filter_A_Z = all(i <= j for i, j in zip(items_all[:-1], items_all[1:]))
        if filter_A_Z:
            print("The filter A-Z works as expected")
            driver.save_screenshot(filename + 'filter_A-Z.png')
        else:
            driver.save_screenshot(filename + 'filter_A-Z_unsuccessful.png')
            print("The filter A-Z doesn't work as expected")

    def test_descending_order_name(self, driver):
        self.login(driver)
        # Find all item_name and check if they are sorted in descending order or not
        driver.find_element(By.CLASS_NAME, select_filter).click()
        driver.find_element(By.XPATH, filter_z_a).click()
        items = driver.find_elements(By.CSS_SELECTOR, ".inventory_item_name")
        items_all = [item.text for item in items]
        filter_Z_A = all(i >= j for i, j in zip(items_all[:-1], items_all[1:]))
        if filter_Z_A:
            driver.save_screenshot(filename + 'filter_Z_A.png')
            print("The filter Z-A works as expected")
        else:
            driver.save_screenshot(filename + 'filter_Z_A_unsuccessful.png')
            print("The filter Z-A doesn't work as expected")

    # 3iv find all prices and look If they are sorted in low to high order or not
    def test_price_ascending(self, driver):
        self.login(driver)
        driver.find_element(By.CLASS_NAME, select_filter).click()
        driver.find_element(By.XPATH, low_to_high).click()
        items = driver.find_elements(By.CSS_SELECTOR, ".inventory_item_price")
        items_all = []
        for item in items:
            item_name = item.text
            items_all.append(item_name)
        normalize_price = [float(re.sub(r"[^\d.]", "", prices)) for prices in items_all]
        filter_price_low_high = all(i <= j for i, j in zip(normalize_price[:-1], normalize_price[1:]))
        if filter_price_low_high:
            driver.save_screenshot(filename + 'filter_price_low_high.png')
            print("The Price (Low to High) filter works as expected")
        else:
            driver.save_screenshot(filename + 'filter_price_low_high_unsuccessful.png')
            print("The Price (Low to High) filter doesn't works as expected")

        # 3iv find all prices and look If they are sorted in high to low order or not
    def test_price_descending(self, driver):
        self.login(driver)
        driver.find_element(By.CLASS_NAME, select_filter).click()
        driver.find_element(By.XPATH, high_to_low).click()
        items = driver.find_elements(By.CSS_SELECTOR, ".inventory_item_price")
        items_all = []
        for item in items:
            item_name = item.text
            items_all.append(item_name)
        normalize_price = [float(re.sub(r"[^\d.]", "", prices)) for prices in items_all]
        filter_price_high_low = all(i >= j for i, j in zip(normalize_price[:-1], normalize_price[1:]))
        if filter_price_high_low:
            driver.save_screenshot(filename + 'filter_price_high_low.png')
            print("The Price (High to Low) filter works as expected")
        else:
            driver.save_screenshot(filename + 'filter_price_high_low_unsuccessful.png')
            print("The Price (High to Low) filter doesn't works as expected")

    # check If the logged-in user can check out or not
    def test_checkout(self, driver):
        self.login(driver)
        driver.find_element(By.ID, checkout).click()
        driver.find_element(By.XPATH, checkout_button).click()
        driver.find_element(By.ID, checkout_first_name).send_keys(first_name)
        driver.find_element(By.ID, checkout_last_name).send_keys(last_name)
        driver.find_element(By.ID, checkout_zip).send_keys(zip_code)
        driver.find_element(By.ID, checkout_continue).click()
        driver.find_element(By.XPATH, checkout_finish).click()
        check_message = driver.find_element(By.XPATH, checkout_message).text
        try:
            assert check_message == "Thank you for your order!"
            print(f"Check out for the {username_value} has been completed successfully!")
            driver.save_screenshot(filename + 'checkout_successful.png')
        except NoSuchElementException as e:
            driver.save_screenshot(filename + 'checkout_unsuccessful.png')
            raise Exception(f"Check out for the {username_value} is unsuccessful!") from e

    def test_locked_users(self, driver):
        driver.get(baseURL)
        wait = WebDriverWait(driver, 60)
        wait.until(EC.visibility_of_element_located((By.XPATH, check_page)))
        driver.find_element(By.ID, username).send_keys(locked_user)
        driver.find_element(By.ID, password).send_keys(password_value)
        driver.find_element(By.ID, submit).click()

        try:
            element = driver.find_element(By.CSS_SELECTOR, error_locked_user).text
            assert element == 'Epic sadface: Sorry, this user has been locked out.'
            print("Can't log in, the user has been locked_out")
            driver.save_screenshot(filename + 'locked_out_user.png')

        except NoSuchElementException as e:
            driver.save_screenshot(filename + 'locked_out_user_login.png')
            raise Exception("Element not found, locked user may be able to log in") from e
