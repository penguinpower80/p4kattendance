import time
import unittest

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class ll_ATS(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_ll(self):
        user = "ngummadi"
        pwd = "isqa8210!"
        driver = self.driver
        driver.maximize_window()
        driver.get("https://p4kids.herokuapp.com/")
        time.sleep(1)
        driver.get("https://p4kids.herokuapp.com/")
        # assert "Logged in"
        driver.find_element_by_xpath(" /html/body/section[1]/div/div/div/div/div/form/p/a ").click()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/section[1]/div/div/form/div/div/input").send_keys('ngummadi@unomaha.edu')
        time.sleep(1)
        driver.find_element_by_xpath('/html/body/section[1]/div/div/form/input[2]').click()
        time.sleep(1)

        try:
            elem = driver.find_element_by_xpath("/html/body/section[1]/div/div/h1")
            text = elem.text
            time.sleep(2)
            assert text == "Check your inbox."

        except NoSuchElementException:
            self.fail("Login Failed - user may not exist")
            assert False
        time.sleep(3)


def tearDown(self):
    self.driver.close()


if __name__ == "__main__":
    unittest.main()