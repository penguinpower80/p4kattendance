import time
import unittest
from select import select
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait


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
        driver.find_element_by_xpath("//*[@id=\"attendancemainnav\"]/div/div[2]/a").click()
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id=\"id_filetype\"]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id=\"id_filetype\"]").send_keys('School File')
        time.sleep(2)
        file_upload = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "id_file")))
        file_upload.send_keys('C:/Users/bharg/OneDrive/Desktop/p4kattendence/p4kattendence/attendance/tests/samples/schools.csv')
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id=\"maincontent\"]/div/div/form/div[3]/button").send_keys('School File')
        time.sleep(2)

        try:
            elem = driver.find_element_by_xpath("//*[@id=\"maincontent\"]/div/div/h2")
            text = elem.text
            time.sleep(2)
            assert text == "Import"

        except NoSuchElementException:
            self.fail("Login Failed - user may not exist")
            assert False
        time.sleep(3)


def tearDown(self):
    self.driver.close()


if __name__ == "__main__":
    unittest.main()


