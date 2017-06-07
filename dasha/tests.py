from unittest import TestCase

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


class MyCase(TestCase):
    def test_signin(self):
        # driver = webdriver.Firefox(executable_path="C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe")
        driver = webdriver.Chrome(executable_path="D:\\chromedriver.exe")
        driver.get("http://127.0.0.1:8000")
        assert "Signin Page" in driver.title
        elem = driver.find_element_by_id("inputEmail")
        elem.clear()
        elem.send_keys("pavlova")

        elem = driver.find_element_by_id("inputPassword")
        elem.clear()
        elem.send_keys(123)

        elem = driver.find_element_by_tag_name("button")
        elem.submit()

        wait = WebDriverWait(driver, 3)
        wait.until(lambda driver: driver.title == "Dasha Project")
        driver.close()
