import time
import unittest

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class ll_ATS(unittest.TestCase):

    def setUp(self):
        #assigning the webdriver to self driver
        self.driver = webdriver.Chrome()

    def test_ll(self):
        user = "Katrina"
        pwd = "Rcb@2022"
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
        # profile
        driver.find_element_by_xpath("/html/body/header/div/div/div[2]/nav/div[2]/div/div[3]/a").click()
        time.sleep(1)



        # Get scroll height
        driver.execute_script("window.scrollTo(0, 250)")
        New_pswrd= "LSG@2022"
        driver.find_element_by_xpath(" /html/body/section[1]/div/div/div/form/div/div/div[4]/div/a ").click()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/section[1]/div/div/div/div/div/form/div[1]/div[1]/div/input").send_keys(pwd)
        time.sleep(1)
        driver.find_element_by_xpath(" /html/body/section[1]/div/div/div/div/div/form/div[1]/div[2]/div/input ").send_keys("New_pswrd")
        time.sleep(1)
        driver.find_element_by_xpath(" /html/body/section[1]/div/div/div/div/div/form/div[1]/div[3]/div/input ").send_keys("New_pswrd")
        time.sleep(1)
        driver.find_element_by_xpath(" /html/body/section[1]/div/div/div/div/div/form/div[2]/button ").click()
        time.sleep(2)




        try:
            elem = driver.find_element_by_xpath(" /html/body/section[1]/div/div/p ")
            text = elem.text
            time.sleep(2)
            assert text == "Your password has been changed!"

        except NoSuchElementException:
            self.fail("Test Case Failed - user may not exist")
            assert False
        time.sleep(3)


def tearDown(self):
    self.driver.close()

if __name__ == "__main__":
    unittest.main()