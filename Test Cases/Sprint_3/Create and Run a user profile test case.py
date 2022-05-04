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
        # First name
        driver.find_element_by_xpath("/html/body/section[1]/div/div/div/form/div/div/div[2]/div[1]/div/div/input").clear()
        time.sleep(1)
        driver.find_element_by_xpath(
            "/html/body/section[1]/div/div/div/form/div/div/div[2]/div[1]/div/div/input").send_keys("Ram Charan")
        time.sleep(1)
        # Last Name
        driver.find_element_by_xpath("/html/body/section[1]/div/div/div/form/div/div/div[2]/div[2]/div/div/input").clear()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/section[1]/div/div/div/form/div/div/div[2]/div[2]/div/div/input").send_keys('Konidela')
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/section[1]/div/div/div/form/div/div/div[3]/div/input").clear()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/section[1]/div/div/div/form/div/div/div[3]/div/input").send_keys("Ramcharan@gmail.com")
        time.sleep(1)

        SCROLL_PAUSE_TIME = 3

        # Get scroll height
        last_height = driver.execute_script("window.scrollTo(0, 250)")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, 250)")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

            #save
        driver.find_element_by_xpath("/html/body/section[1]/div/div/div/form/div/div/div[5]/div/div/div/button").click()




        try:
            elem = driver.find_element_by_xpath("/html/body/section[1]/div/div/h2")
            text = elem.text
            time.sleep(2)
            assert text == "My Profile"

        except NoSuchElementException:
            self.fail("Test Case Failed - user may not exist")
            assert False
        time.sleep(3)


def tearDown(self):
    self.driver.close()

if __name__ == "__main__":
    unittest.main()