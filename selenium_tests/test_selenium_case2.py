 

import time
import os
import logging
from datetime import datetime
from typing import Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    UnexpectedAlertPresentException
)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TestSeleniumPractice:
    """
    Selenium Practice Lab Test Suite
    
    This class contains all test methods for practicing Selenium automation
    with a React-based frontend application.
    
    Run with pytest:
        pytest test_selenium_practice.py -v
    """
    
    base_url = os.environ.get("BASE_URL", "https://react-selenium-automation.replit.app/")
    driver: Optional[webdriver.Chrome] = None
    wait: Optional[WebDriverWait] = None
    screenshots_dir = "screenshots"
    
    def setup_method(self) -> None:
        """
        Set up the WebDriver with appropriate options.
        
        Configures Chrome WebDriver with:
        - Headless mode (optional)
        - Window size
        - Implicit wait (global)
        """
        os.makedirs(self.screenshots_dir, exist_ok=True)
        
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        
        self.driver.implicitly_wait(5)
        
        self.wait = WebDriverWait(self.driver, 10)
        
        logger.info("WebDriver initialized successfully")
    
    def teardown_method(self) -> None:
        """Clean up resources and close the browser."""
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver closed")
    
    def test_dynamic_element_loading(self) -> bool:
        """
        Test 1: Dynamic Element Loading with Explicit Wait
        
        This test demonstrates:
        - WebDriverWait with expected_conditions
        - Waiting for elements to be clickable
        - Handling delayed element rendering (2 seconds)
        
        Returns:
            bool: True if test passes, False otherwise
        """
        logger.info("=" * 50)
        logger.info("Test 1: Dynamic Element Loading")
        logger.info("=" * 50)
        
        try:
            self.driver.get(self.base_url)
            
            load_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='button-load-elements']"))
            )
            logger.info("Found load button using data-testid selector")
            
            load_button.click()
            logger.info("Clicked load button - waiting 2 seconds for dynamic elements...")
            
            dynamic_input = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='input-dynamic']"))
            )
            logger.info("Dynamic input appeared!")
            
            dynamic_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='button-dynamic-action']"))
            )
            logger.info("Dynamic button is clickable!")
            
            dynamic_message = self.driver.find_element(
                By.CSS_SELECTOR, "[data-testid='text-dynamic-message']"
            )
            assert "successfully" in dynamic_message.text.lower()
            logger.info(f"Success message verified: {dynamic_message.text}")
            
            logger.info("TEST PASSED: Dynamic Element Loading")
            # return True
            
            target_input = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-element-type="delayed-input"]')))
            target_input.clear()
            target_input.send_keys("피카츄")
                
            time.sleep(3)
            
        except Exception as e:
            logger.error(f"TEST FAILED: {str(e)}")
            self.save_screenshot("test_dynamic_loading_failed")
            return False
    
    def test_state_controlled_inputs(self) -> bool:
        """
        Test 2: React State-Controlled Input Handling
        
        This test demonstrates:
        - send_keys() for React controlled inputs
        - Verifying React state updates
        - Form submission
        
        Important: Direct DOM value manipulation won't work with React!
        You must use send_keys() to trigger onChange events.
        
        Returns:
            bool: True if test passes, False otherwise
        """
        logger.info("=" * 50)
        logger.info("Test 2: State-Controlled Input Handling")
        logger.info("=" * 50)
        
        try:
            self.driver.get(self.base_url)
            
            username_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='input-username']"))
            )
            
            password_input = self.driver.find_element(
                By.CSS_SELECTOR, "[data-testid='input-password']"
            )
            
            test_username = "selenium_user"
            test_password = "secure_password_123"
            
            username_input.clear()
            username_input.send_keys(test_username)
            logger.info(f"Entered username: {test_username}")
            
            password_input.clear()
            password_input.send_keys(test_password)
            logger.info("Entered password")
            
            username_state = self.driver.find_element(
                By.CSS_SELECTOR, "[data-testid='text-username-state']"
            )
            assert test_username in username_state.text
            logger.info(f"State verification: Username state shows '{username_state.text}'")
            
            password_state = self.driver.find_element(
                By.CSS_SELECTOR, "[data-testid='text-password-state']"
            )
            expected_masked = "*" * len(test_password)
            assert expected_masked in password_state.text
            logger.info("State verification: Password state shows masked value")
            
            login_button = self.driver.find_element(
                By.CSS_SELECTOR, "[data-testid='button-login']"
            )
            login_button.click()
            logger.info("Clicked login button")
            
            result_element = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='text-login-result']"))
            )
            assert "successful" in result_element.text.lower()
            logger.info(f"Login result: {result_element.text}")
            
            logger.info("TEST PASSED: State-Controlled Inputs")
            # return True
            time.sleep(3)
            
        except Exception as e:
            logger.error(f"TEST FAILED: {str(e)}")
            self.save_screenshot("test_state_inputs_failed")
            return False
    

if __name__ == "__main__":
    exit(main())
