'''
Feature: Projects and experiments should be creatable and deletable

  Scenario: Successful Login
     Given i navigate to next.discovery
      When i login with valid email and password
      Then i should redirect to see "Dashboard"

  Scenario: Create Project
     Given i am logged into Dashboard
      When i click new project
      Then i should see "Create project page"
      And i should be able to create the project

  Scenario: Invalid Create Experiment
     Given i have created a proejct
      When i click new experiment
      Then  i should see "Oops, you haven't uploaded a target set yet!"

  Scenario: Upload Target CSV
     Given i have created a proejct
      When i click manage targets
      And  i upload animals.csv
      Then i should see "218" targets in target set

  Scenario: Valid Create Experiment
     Given i have created a proejct
      When i click new experiment
      And  i have uploaded a target set
      Then i should be able to successfully create "example experiment" PoolBasedTripletMDS experiment

  Scenario: Created Experiment in Staging
     Given i have created an experiment
      When i click my experiment
      Then i should see "Status: Staging"

  Scenario: Run Created Experiment
     Given i have created an experiment
      And  i have my experiment in staging
      When i click "start experiment"
      Then i should see "Status: Running"

  Scenario: Non-Reckless Delete Created Project
     Given i am running an experiment in a project
      When i click "delete project"
      Then i should see "Are you sure you want to delete project?"

  Scenario: Delete Created Project
     Given i am running an experiment in a project
      When i click "delete project"
      And  i see "Are you sure you want to delete project?" 
      And  i click "delete"
      Then i should not see a project named "example project 4"          
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class CreateProjCreateExpEw5(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://ec2-54-69-195-202.us-west-2.compute.amazonaws.com:8002"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_create_proj_create_exp_ew5(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys("fez_test")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("foo")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        #driver.find_element_by_id("password").clear()
        #driver.find_element_by_id("password").send_keys("foo")
        #driver.find_element_by_css_selector("button.btn.btn-primary").click()
        driver.find_element_by_xpath("//a[contains(@href, '/new_project/')]").click()
        driver.find_element_by_id("name").clear()
        driver.find_element_by_id("name").send_keys("example project 4")
        driver.find_element_by_id("description").clear()
        driver.find_element_by_id("description").send_keys("this is an example project for BD testing")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        try: self.assertEqual("Project: example project 4", driver.find_element_by_css_selector("h1.page-header").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_xpath("//a[contains(@href, '/new_experiment/')]").click()
        for i in range(60):
            try:
                if "NEXT.Discovery New Experiment" == driver.title: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("Oops, you haven't uploaded a target set yet!", driver.find_element_by_css_selector("h4").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_xpath("//a[contains(@href, '/targets/manage')]").click()
        #driver.find_element_by_name("hosted_csv_file").clear()
        driver.find_element_by_name("hosted_csv_file").send_keys("/home/chris/Downloads/animals.csv")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        try: self.assertEqual("218", driver.find_element_by_xpath("//div[@id='page-wrapper']/div/div/table/tbody/tr/td[2]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_xpath("//a[contains(@href, '/new_experiment/')]").click()
        for i in range(60):
            try:
                if "NEXT.Discovery New Experiment" == driver.title: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("First you need to decide what type of experiment you would like to create:", driver.find_element_by_css_selector("div.description").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_xpath("//a[contains(@href, '/new_experiment/PoolBasedTripletMDS')]").click()
        driver.find_element_by_id("name").clear()
        driver.find_element_by_id("name").send_keys("example experiment")
        driver.find_element_by_id("description").clear()
        driver.find_element_by_id("description").send_keys("this is an example experiment for BD testing")
        driver.find_element_by_id("instructions").clear()
        driver.find_element_by_id("instructions").send_keys("start the experiment")
        driver.find_element_by_id("debrief").clear()
        driver.find_element_by_id("debrief").send_keys("thanks for participating!")
        driver.find_element_by_id("query_tries").clear()
        driver.find_element_by_id("query_tries").send_keys("10")
        driver.find_element_by_id("query_duration").clear()
        driver.find_element_by_id("query_duration").send_keys("5")
        driver.find_element_by_id("params-d").clear()
        driver.find_element_by_id("params-d").send_keys("2")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        for i in range(60):
            try:
                if "Status: Staging" == driver.find_element_by_xpath("//div[@id='page-wrapper']/div/div/div[2]/div/p").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("Status: Staging", driver.find_element_by_xpath("//div[@id='page-wrapper']/div/div/div[2]/div/p").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("a.btn.btn-primary").click()
        for i in range(60):
            try:
                if "Status: Running" == driver.find_element_by_xpath("//div[@id='page-wrapper']/div/div/div[2]/div/p").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("Status: Running", driver.find_element_by_xpath("//div[@id='page-wrapper']/div/div/div[2]/div/p").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_xpath("//a[contains(@href, '/dashboard/')]").click()
        for i in range(60):
            try:
                if self.is_element_present(By.CSS_SELECTOR, "h1.page-header"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        driver.find_element_by_xpath("(//button[@type='button'])[10]").click()
        driver.find_element_by_xpath("(//button[@value='delete'])[5]").click()
    
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
