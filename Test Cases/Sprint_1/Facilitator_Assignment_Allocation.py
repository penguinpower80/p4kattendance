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
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id=\"maincontent\"]/div/div/div/div/div/form/div[2]/button").click()
        time.sleep(1)
        driver.get("https://p4kids.herokuapp.com/")
        # assert "Logged in"
        driver.find_element_by_xpath("//*[@id=\"maincontent\"]/div/div/div/div[1]/a[3]").click()
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id=\"maincontent\"]/div/div/div/div[1]/div/a[1]").click()
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id=\"school-item-28-0001-225\"]/div[1]/a").click()
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id=\"classroom-item-1\"]/div[1]/a").click()
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id=\"classroom-1\"]/div/div[3]/label/input").click()
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id=\"maincontent\"]/div/div/form/div[1]/div[2]/button").click()
        time.sleep(3)

        try:
            elem = driver.find_element_by_xpath("//*[@id=\"maincontent\"]/div/div/h2")
            text = elem.text
            time.sleep(2)
            assert text == "Assignments"

        except NoSuchElementException:
            self.fail("Login Failed - user may not exist")
            assert False
        time.sleep(3)


def tearDown(self):
    self.driver.close()

if __name__ == "__main__":
    unittest.main()