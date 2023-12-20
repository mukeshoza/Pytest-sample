import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import datetime
from locators import *
import re

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("--hide-scrollbars")
# options.add_argument("--headless")

baseURL = 'https://www.saucedemo.com/'
file_path = os.path.dirname(os.path.dirname(__file__))
filename = os.path.join(file_path, 'leapfrog_assesment/screenshots/')


class SeleniumTest:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 60)

    def login_standard_user(self):
        self.driver.get(baseURL)
        time_start = datetime.datetime.now()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, check_page)))

        # 1 check if the user can login into the page or not
        self.driver.find_element(By.ID, username).send_keys(username_value)
        self.driver.find_element(By.ID, password).send_keys(password_value)
        self.driver.find_element(By.ID, submit).click()

        try:
            element = self.driver.find_element(By.CLASS_NAME, product_page)
            assert element.is_displayed()
            print(f"Sign in Successful with username {username_value}")
            self.driver.save_screenshot(filename + 'sign_in_successful.png')
        except NoSuchElementException as e:
            self.driver.save_screenshot(filename + 'sign_in_unsuccessful.png')
            raise Exception(f"Sign in Unsuccessful with username {username_value}") from e

        # 2 check if the items can be added in the cart by logged-in user or not
        self.driver.find_element(By.ID, add_to_cart).click()
        self.driver.find_element(By.ID, add_to_cart_1).click()
        check_cart = self.driver.find_element(By.CLASS_NAME, cart_value).text
        try:
            assert check_cart == "2"
            print(f"{username_value} can add items to cart")
            self.driver.save_screenshot(filename + 'add_to_cart.png')
        except NoSuchElementException as e:
            self.driver.save_screenshot(filename + 'add_to_cart_unsuccessful.png')
            raise Exception(f"{username_value} can't add items to cart") from e

        # 3i find all item_name and look If they are sorted in ascending order or not
        items = self.driver.find_elements(By.CSS_SELECTOR, ".inventory_item_name")
        items_all = []
        for item in items:
            item_name = item.text
            items_all.append(item_name)
        # is_sorted = items_all = sorted(items_all)
        filter_A_Z = all(i <= j for i, j in zip(items_all[:-1], items_all[1:]))
        if filter_A_Z:
            print("The filter A-Z works as expected")
            self.driver.save_screenshot(filename + 'filter_A-Z.png')
        else:
            self.driver.save_screenshot(filename + 'filter_A-Z_unsuccessful.png')
            print("The filter A-Z doesn't works as expected")

        # 3ii find all item_name and look If they are sorted in descending order or not
        self.driver.find_element(By.CLASS_NAME, select_filter).click()
        self.driver.find_element(By.XPATH, filter_z_a).click()
        items = self.driver.find_elements(By.CSS_SELECTOR, ".inventory_item_name")
        items_all = []
        for item in items:
            item_name = item.text
            items_all.append(item_name)
        filter_Z_A = all(i >= j for i, j in zip(items_all[:-1], items_all[1:]))
        if filter_Z_A:
            self.driver.save_screenshot(filename + 'filter_Z_A.png')
            print("The filter Z-A works as expected")
        else:
            self.driver.save_screenshot(filename + 'filter_Z_A_unsuccessful.png')
            print("The filter Z-A doesn't works as expected")

        # 3iii find all prices and look If they are sorted in high to low order or not
        self.driver.find_element(By.CLASS_NAME, select_filter).click()
        self.driver.find_element(By.XPATH, low_to_high).click()
        items = self.driver.find_elements(By.CSS_SELECTOR, ".inventory_item_price")
        items_all = []
        for item in items:
            item_name = item.text
            items_all.append(item_name)
        normalize_price = [float(re.sub(r"[^\d.]", "", prices)) for prices in items_all]
        filter_price_low_high = all(i <= j for i, j in zip(normalize_price[:-1], normalize_price[1:]))
        if filter_price_low_high:
            self.driver.save_screenshot(filename + 'filter_price_low_high.png')
            print("The Price (Low to High) filter works as expected")
        else:
            self.driver.save_screenshot(filename + 'filter_price_low_high_unsuccessful.png')
            print("The Price (Low to High) filter doesn't works as expected")

        # 3iv find all prices and look If they are sorted in low to high order or not
        self.driver.find_element(By.CLASS_NAME, select_filter).click()
        self.driver.find_element(By.XPATH, high_to_low).click()
        items = self.driver.find_elements(By.CSS_SELECTOR, ".inventory_item_price")
        items_all = []
        for item in items:
            item_name = item.text
            items_all.append(item_name)
        normalize_price = [float(re.sub(r"[^\d.]", "", prices)) for prices in items_all]
        filter_price_high_low = all(i >= j for i, j in zip(normalize_price[:-1], normalize_price[1:]))
        if filter_price_high_low:
            self.driver.save_screenshot(filename + 'filter_price_high_low.png')
            print("The Price (High to Low) filter works as expected")
        else:
            self.driver.save_screenshot(filename + 'filter_price_high_low_unsuccessful.png')
            print("The Price (High to Low) filter doesn't works as expected")

        # check If the logged-in user can check out or not
        self.driver.find_element(By.ID, checkout).click()
        # self.driver.find_element(By.CLASS_NAME, cart_item)
        self.driver.find_element(By.XPATH, checkout_button).click()
        self.driver.find_element(By.ID, checkout_first_name).send_keys(first_name)
        self.driver.find_element(By.ID, checkout_last_name).send_keys(last_name)
        self.driver.find_element(By.ID, checkout_zip).send_keys(zip_code)
        self.driver.find_element(By.ID, checkout_continue).click()
        self.driver.find_element(By.XPATH, checkout_finish).click()
        check_message = self.driver.find_element(By.XPATH, checkout_message).text
        try:
            assert check_message == "Thank you for your order!"
            print(f"Check out for the {username_value} has been completed successfully!")
            self.driver.save_screenshot(filename + 'checkout_successful.png')
        except NoSuchElementException as e:
            self.driver.save_screenshot(filename + 'checkout_unsuccessful.png')
            raise Exception(f"Check out for the {username_value} is unsuccessful!") from e

        time_end = datetime.datetime.now()
        total_time_taken = time_end - time_start
        time_sec = round((total_time_taken.total_seconds() / 60.0), 3)
        print(f'Total time taken to complete the test: {time_sec} seconds')
        print('==========================================================')

    def locked_users(self):
        self.driver.get(baseURL)
        time_start = datetime.datetime.now()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, check_page)))

        # 1 check if the user can login into the page or not
        self.driver.find_element(By.ID, username).send_keys(locked_user)
        self.driver.find_element(By.ID, password).send_keys(password_value)
        self.driver.find_element(By.ID, submit).click()

        try:
            element = self.driver.find_element(By.CSS_SELECTOR, error_locked_user).text
            assert element == 'Epic sadface: Sorry, this user has been locked out.'
            print("Can't log in, the user has been locked_out")
            self.driver.save_screenshot(filename + 'locked_out_user.png')

        except NoSuchElementException as e:
            self.driver.save_screenshot(filename + 'locked_out_user_login.png')
            raise Exception("Element not found, locked user may be able to log in") from e

        time_end = datetime.datetime.now()
        total_time_taken = time_end - time_start
        time_sec = round((total_time_taken.total_seconds() / 60.0), 3)
        print(f'Total time taken to complete the test: {time_sec} seconds')
        print('==========================================================')

    def quit_browser(self):
        self.driver.quit()


test = SeleniumTest()
test.login_standard_user()
test.locked_users()
test.quit_browser()
