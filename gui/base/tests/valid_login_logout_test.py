'''
Feature: As an application that collects research data,
            I want to secure authentication

  Scenario: Successful Login
     Given i navigate to next.discovery
      When i login with valid email and password
      Then i should redirect to see "Dashboard"

  Scenario: Logout
     Given i navigate to next.discovery
     and i login with valid email and password
      When i logout
      Then  i should see the alert "You were logged out"

Needed Scenarios:

  Scenario: Successful Account creation
     Given i navigate to next.discovery
      When i create account with valid email and password
      Then i should see the alert "Account created"

  Scenario: Unccessful Account creation, email
     Given i navigate to next.discovery
      When i create account with an invalid email and valid passwords
      Then i should see the alert "Email already in use"

  Scenario: Unccessful Account creation, passwords
     Given i navigate to next.discovery
      When i create account with an valid email and non-matching password and confirm password
      Then i should see the alert "Passwords do not match"

  Scenario: Incorrect Username
     Given i navigate to next.discovery
      When i login with invalid email and password
      Then i should see the alert "Invalid username"

  Scenario: Incorrect Password
     Given i navigate to next.discovery
      When i login with valid email and invalid password
      Then  i should see the alert "Invalid password"
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class Login3(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://ec2-54-69-195-202.us-west-2.compute.amazonaws.com:8002"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_login3(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys("fez_test")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("foo")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        self.assertEqual("Dashboard", driver.find_element_by_css_selector("h1.page-header").text)
        for i in range(60):
            try:
                if self.is_element_present(By.XPATH, "//a[contains(@href, '/logout')]"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        driver.find_element_by_xpath("//a[contains(@href, '/logout')]").click()
        self.assertEqual("NEXT.discovery", driver.title)
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
