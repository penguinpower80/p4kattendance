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
        # assert "Logged in"
        driver.find_element_by_xpath(" /html/body/header/div/div/div[2]/nav/div[2]/div/div[5]/a ").click()
        time.sleep(1)
        driver.find_element_by_xpath(" /html/body/section[1]/div/div/div/div/a[1] ").click()
        time.sleep(1)
        driver.find_element_by_xpath(" /html/body/section[1]/div/div/form/div[1]/div/div/div/select ").send_keys("school")
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/section[1]/div/div/form/div[2]/div[1]/div/div/select").send_keys("SHERMAN ELEM SCHOOL")
        driver.find_element_by_xpath(" /html/body/section[1]/div/div/form/div[3]/div[1]/div/div[1]/div/input[1]").click()
        driver.find_element_by_xpath("/html/body/section[1]/div/div/form/div[3]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div[6]/button").click()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/section[1]/div/div/form/div[3]/div[2]/div/div[1]/div/input[1]").click()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/section[1]/div/div/form/div[3]/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div[13]").click()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/section[1]/div/div/form/div[4]/div/button/span[2]").click()
        time.sleep(1)

        try:
            elem = driver.find_element_by_xpath("/html/body/section[1]/div/div/div[1]/div[1]/h2")
            text = elem.text
            time.sleep(2)
            assert text == "Report: Notes"

        except NoSuchElementException:
            self.fail("Login Failed - user may not exist")
            assert False
        time.sleep(3)


def tearDown(self):
    self.driver.close()


if __name__ == "__main__":
    unittest.main()