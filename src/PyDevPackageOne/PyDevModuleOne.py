'''
Created on Nov 6, 2020

@author: Chris Luhring
Eclipse / Python setup: https://www.vogella.com/tutorials/Python/article.html
Unit Test: https://blog.testproject.io/2016/12/08/using-selenium-with-python-p2/
Pip: https://pip.pypa.io/en/stable/installing/
Selenium: https://selenium-python.readthedocs.io/installation.html
'''
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Test(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Firefox()
        
    def tearDown(self):
        self.driver.quit()
    
        def centerElement(self, element):
        driver = self.driver
        desired_y = (element.size['height'] / 2) + element.location['y']
        window_h = driver.execute_script('return window.innerHeight')
        window_y = driver.execute_script('return window.pageYOffset')
        current_y = (window_h / 2) + window_y
        scroll_y_by = desired_y - current_y
        driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
        
    def testGuild(self):
        driver = self.driver
        driver.get("https://www.guildeducation.com/")
        assert "Education as a Benefit - Guild Education" in driver.title, "FAIL: Incorrect Title"
        print("PASS:  Found Guild Edu URL")

        # Find Get Started Button / CenterElement / Click
        get_started_button = driver.find_element_by_link_text("Get Started")
        self.centerElement(get_started_button)        
        assert get_started_button.is_enabled, "FAIL: 'Get Started' Button is not enabled on Guild Home Page"
        get_started_button.click()
        
        # Ensure now on interested partner page
        assert "https://resource.guildeducation.com/interested_partner" in driver.current_url, "FAIL: Incorrect Redirect"
        print("PASS:  Clicked on 'Get Started' button, correctly redirected")

        # Wait for Venmo Player
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#lp-pom-video-566 iframe")))

        # Center / Play Video
        venmo_player = driver.find_element_by_css_selector("div#lp-pom-video-566 iframe")
        self.centerElement(venmo_player)
        
        # Play / Pause
        driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
        self.assertTrue(driver.find_element_by_css_selector("button.play div.play-icon").is_displayed(), 
                        "FAIL: Play Button is not Visible prior to playing Video")
        self.assertFalse(driver.find_element_by_css_selector("div.pause-icon").is_displayed(), 
                         "FAIL: Pause Button is Visible prior to playing Video")
        driver.find_element_by_css_selector("button.play").click()
        self.assertTrue(driver.find_element_by_css_selector("div.pause-icon").is_displayed(), 
                        "FAIL: Pause Button is not Visible after playing Video")
        self.assertFalse(driver.find_element_by_css_selector("div.play-icon").is_displayed(), 
                         "FAIL: Play Button is Visible after playing Video")
        print("PASS:  Venmo Player working correctly")

        time.sleep(4)
        
        ## Switch back to the "default content" (that is, out of the iframes) ##
        driver.switch_to.default_content()
        
        # Marketing Form Check - Required Field
        request_info_btn = driver.find_element_by_css_selector("button.mktoButton")
        self.centerElement(request_info_btn)
        request_info_btn.click()
        print("PASS:  Clicked on mktoForm_1076 Submit Button")
        
        # First Name Input - Required
        first_name_input = driver.find_element_by_css_selector("input#FirstName")
        self.assertTrue("mktoRequired" in first_name_input.get_attribute("class"),
                         "FAIL: First Name Input not Required")
        first_name_input.click()
        first_name_error = driver.find_element_by_css_selector("div#ValidMsgFirstName")
        self.assertTrue(first_name_error.is_displayed(), "FAIL: First Name Error Message is Not Displayed")
        self.assertEqual(first_name_error.text, "This field is required.", 
                         "FAIL : First Name Error Message contains incorrect Text")
        print("PASS:  Found Correct Form: First Name Error Message")

        
