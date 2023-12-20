import os
import datetime
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


@pytest.fixture
def driver():
    driver_instance = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver_instance.maximize_window()
    yield driver_instance
    driver_instance.quit()


def test_login_standard_user(driver):
    driver.get(baseURL)
    time_start = datetime.datetime.now()
    wait = WebDriverWait(driver, 60)
    wait.until(EC.visibility_of_element_located((By.XPATH, check_page)))

    # 1 check if the user can log in into the page or not
    driver.find_element(By.ID, username).send_keys(username_value)
    driver.find_element(By.ID, password).send_keys(password_value)
    driver.find_element(By.ID, submit).click()

    try:
        element = driver.find_element(By.CLASS_NAME, product_page)
        assert element.is_displayed()
        print("Sign in Successful with username")
    except NoSuchElementException as e:
        driver.save_screenshot(filename + 'sign_in_unsuccessful.png')
        raise Exception("Sign in Unsuccessful") from e


def test_add_to_cart(driver):
    # 2 check if the items can be added in the cart by a logged-in user or not
    driver.get(baseURL)
    time_start = datetime.datetime.now()
    wait = WebDriverWait(driver, 60)
    wait.until(EC.visibility_of_element_located((By.XPATH, check_page)))

    # 1 check if the user can log in into the page or not
    driver.find_element(By.ID, username).send_keys(username_value)
    driver.find_element(By.ID, password).send_keys(password_value)
    driver.find_element(By.ID, submit).click()
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


# test = TestSelenium()
# test.test_login_standard_user()
# test.test_add_to_cart()
# test.test_locked_users()
