import datetime
import time
import unittest
from telnetlib import EC

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


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

        driver.find_element(By.XPATH, "//*[@id=\"id_username\"]").send_keys(user)
        driver.find_element(By.XPATH, "//*[@id=\"id_password\"]").send_keys(pwd)
        driver.find_element(By.XPATH, "//*[@id=\"maincontent\"]/div/div/div/div/div/form/div[2]/button").click()
        time.sleep(1)


        driver.find_element(By.CSS_SELECTOR, '.note-trigger').click()
        time.sleep(2)
        driver.switch_to.frame(0)
        driver.find_element(By.CSS_SELECTOR, "html").click()
        element = driver.find_element(By.CSS_SELECTOR, ".cke_editable")
        element.send_keys('TESTING P4K')
        driver.switch_to.default_content()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, ".savenote").click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, '.note-trigger').click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, '.listnotes').click()
        time.sleep(1)
        all_note_text = driver.find_element(By.ID, 'noteslist').text
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, '.deletenote').click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, '.swal2-confirm').click()
        time.sleep(1)
        assert 'TESTING P4K' in all_note_text


        time.sleep(5)


def tearDown(self):



    self.driver.close()


if __name__ == "__main__":
    unittest.main()