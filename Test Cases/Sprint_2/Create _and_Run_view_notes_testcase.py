import time
import unittest

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class ll_ATS(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_ll(self):
        user = "Katrina"
        pwd = "Rcb@2022"
        driver = self.driver
        driver.maximize_window()
        driver.get("https://p4kids.herokuapp.com/")
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/section[1]/div/div/div/div/div/form/div[1]/div[1]/div/input").send_keys(user)
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/section[1]/div/div/div/div/div/form/div[1]/div[2]/div/input").send_keys(pwd)
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/section[1]/div/div/div/div/div/form/div[2]/button").click()
        time.sleep(1)
        driver.get("https://p4kids.herokuapp.com/")
        # assert "Logged in"
        driver.find_element_by_xpath("/html/body/section[1]/div/div/div/article/div[1]/a").click()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/section[1]/div/div/div/article/div[2]/div/article/div[1]/a").click()
        time.sleep(1)
        #notes
        driver.find_element_by_xpath("/html/body/section[1]/div/div/div/article/div[2]/div/article/div[2]/div/div/a").click()
        driver.find_element_by_xpath("/html/body/div[1]/div[2]/footer/button[1]/span").click()
        time.sleep(3)
        driver.find_element_by_xpath("/html/body/div[1]/div[2]/section/div[2]").click()
        time.sleep(2)

        try:
            elem = driver.find_element_by_xpath('/html/body/div[1]/div[2]/header/p')
            text = elem.text
            # attempt to find the 'Logout' button - if found, logged in

            time.sleep(2)
            assert text == "Emily Stevens"

        except NoSuchElementException:
            self.fail("Test case failed")
            assert False
        time.sleep(3)

    def tearDown(self):
        self.driver.close()

