import time
import unittest

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class ll_ATS(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_ll(self):
        user = "p4kadmin"
        pwd = "isqa8210!"
        driver = self.driver
        driver.maximize_window()
        driver.get("https://p4kids.herokuapp.com/")
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id=\"id_username\"]").send_keys(user)
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id=\"id_password\"]").send_keys(pwd)
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id=\"maincontent\"]/div/div/div/div/div/form/div[2]/button").click()
        time.sleep(1)
        driver.get("https://p4kids.herokuapp.com/")
        time.sleep(1)
        driver.get("https://p4kids.herokuapp.com/accounts/logout")
        time.sleep(1)

        # assert "Logged in"
        #Mentor Login-
        user1 = "bprice"
        pwd1 = "Rcb@2022"
        driver = self.driver
        driver.maximize_window()
        driver.get("https://p4kids.herokuapp.com/")
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id=\"id_username\"]").send_keys(user1)
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id=\"id_password\"]").send_keys(pwd1)
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id=\"maincontent\"]/div/div/div/div/div/form/div[2]/button").click()
        time.sleep(1)
        driver.get("https://p4kids.herokuapp.com/accounts/logout")
        time.sleep(1)

        # FAcilitator Login-
        user1 = "bgarcia"
        pwd1 = "Rcb@2022"
        driver = self.driver
        driver.maximize_window()
        driver.get("https://p4kids.herokuapp.com/")
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id=\"id_username\"]").send_keys(user1)
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id=\"id_password\"]").send_keys(pwd1)
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id=\"maincontent\"]/div/div/div/div/div/form/div[2]/button").click()
        time.sleep(1)
        driver.get("https://p4kids.herokuapp.com/accounts/logout")
        time.sleep(1)

        try:
            elem = driver.find_element_by_xpath("/html/body/section[1]/div/div/div/div/div/form/h2")
            text = elem.text
            time.sleep(2)
            assert text == "Log In"

        except NoSuchElementException:
            self.fail("Login Failed - user may not exist")
            assert False
        time.sleep(3)


def tearDown(self):
    self.driver.close()


if __name__ == "__main__":
    unittest.main()