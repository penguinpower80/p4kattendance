import datetime
import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By


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
        driver.get("https://p4kids.herokuapp.com/meeting/student/3249783830")
        time.sleep(1)
        # could use meeting id to check DB if had access:
        self.meeting_id = driver.find_element(By.CSS_SELECTOR, ".deletemeeting").get_attribute('data-rel')
        original_value = driver.find_element(By.ID, "meeting_date").get_attribute('value')
        driver.find_element(By.CSS_SELECTOR, ".datetimepicker-dummy-input").click()
        time.sleep(1)

        d = datetime.datetime.now()
        current_day = d.strftime("%d")
        if current_day != '1':
            # if it is the first of the month, then pick a DIFFERENT day!
            driver.find_element(By.CSS_SELECTOR, ".is-current-month > .date-item").click()
        else:
            # otherwise pick the first day of the month
            driver.find_element(By.CSS_SELECTOR, ".is-current-month + div > .date-item").click()

        new_value = driver.find_element(By.ID, "meeting_date").get_attribute('value')
        print(self.meeting_id)
        driver.get("https://p4kids.herokuapp.com/meeting/delete/" + self.meeting_id)
        time.sleep(2)
        if original_value != new_value:
            assert True
        else:
            self.fail("Meeting date did not change.")
            assert False


def tearDown(self):



    self.driver.close()


if __name__ == "__main__":
    unittest.main()