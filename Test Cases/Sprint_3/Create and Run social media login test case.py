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
        # Get scroll height
        driver.execute_script("window.scrollTo(0, 250)")
        time.sleep(1)
        # assert "Logged in"
        driver.find_element_by_xpath(" /html/body/section[1]/div/div/div/div/div/div/div/div[1]/a ").click()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input").send_keys("ngummadi@unomaha.edu   ")
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/span").click()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div/main/div/div[2]/form/input[1]").send_keys('Please use yout uno mail id')
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div/main/div/div[2]/form/input[2]").send_keys("Please give your password")
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div/main/div/div[2]/form/button").click()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div/div/div[1]/div/form/div[1]/fieldset[1]/div[1]/button").click()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/span").click()

        time.sleep(1555)


        try:
            elem = driver.find_element_by_xpath("//*[@id=\"maincontent\"]/div/div/h1")
            text = elem.text
            time.sleep(2)
            assert text == "Welcome"

        except NoSuchElementException:
            self.fail("Login Failed - user may not exist")
            assert False
        time.sleep(3)


def tearDown(self):
    self.driver.close()


if __name__ == "__main__":
    unittest.main()