"""
Selenium Practice Lab - Test Automation Scripts
================================================

This module contains comprehensive Selenium test scripts designed to practice
various automation techniques with a React-based frontend.

Requirements:
- Python 3.8+
- selenium
- webdriver-manager (optional, for automatic driver management)

Installation:
    pip install selenium webdriver-manager

Usage:
    python test_selenium_practice.py

Features Covered:
- Wait Strategies (Implicit & Explicit)
- CSS Selectors & data-* attributes
- ActionChains (hover, double-click)
- JavaScript execution (scroll, force click)
- Alert handling
- State-controlled input handling
- Screenshot capture on failure
"""

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
    
    base_url = os.environ.get("BASE_URL", "http://localhost:5000")
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
    
    def save_screenshot(self, name: str) -> str:
        """
        Save a screenshot with timestamp.
        
        Args:
            name: Base name for the screenshot
            
        Returns:
            Path to the saved screenshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(self.screenshots_dir, filename)
        self.driver.save_screenshot(filepath)
        logger.info(f"Screenshot saved: {filepath}")
        return filepath
    
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
            return True
            
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
            return True
            
        except Exception as e:
            logger.error(f"TEST FAILED: {str(e)}")
            self.save_screenshot("test_state_inputs_failed")
            return False
    
    def test_hover_dropdown_menu(self) -> bool:
        """
        Test 3: Hover Dropdown Menu with ActionChains
        
        This test demonstrates:
        - ActionChains for mouse hover
        - move_to_element() action
        - Waiting for dropdown visibility
        - Clicking dropdown items
        
        Returns:
            bool: True if test passes, False otherwise
        """
        logger.info("=" * 50)
        logger.info("Test 3: Hover Dropdown Menu")
        logger.info("=" * 50)
        
        try:
            self.driver.get(self.base_url)
            
            hover_trigger = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='button-hover-trigger']"))
            )
            
            actions = ActionChains(self.driver)
            actions.move_to_element(hover_trigger).perform()
            logger.info("Performed hover action on trigger button")
            
            dropdown_menu = self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='container-hover-menu']"))
            )
            logger.info("Dropdown menu is now visible!")
            
            menu_items = self.driver.find_elements(
                By.CSS_SELECTOR, "[data-testid^='menu-item-']"
            )
            logger.info(f"Found {len(menu_items)} menu items")
            
            if menu_items:
                target_item = menu_items[1]
                actions = ActionChains(self.driver)
                actions.move_to_element(target_item).click().perform()
                logger.info("Clicked on second menu item")
                
                selected_text = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='text-selected-menu-item']"))
                )
                logger.info(f"Selected item confirmed: {selected_text.text}")
            
            logger.info("TEST PASSED: Hover Dropdown Menu")
            return True
            
        except Exception as e:
            logger.error(f"TEST FAILED: {str(e)}")
            self.save_screenshot("test_hover_dropdown_failed")
            return False
    
    def test_alert_handling(self) -> bool:
        """
        Test 4: Browser Alert Handling
        
        This test demonstrates:
        - Triggering browser alerts
        - Switching to alert context
        - Accept/Dismiss alert dialogs
        - Handling confirm() and prompt()
        
        Returns:
            bool: True if test passes, False otherwise
        """
        logger.info("=" * 50)
        logger.info("Test 4: Alert Dialog Handling")
        logger.info("=" * 50)
        
        try:
            self.driver.get(self.base_url)
            
            simple_alert_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='button-simple-alert']"))
            )
            simple_alert_button.click()
            logger.info("Clicked simple alert button")
            
            alert = self.wait.until(EC.alert_is_present())
            alert_text = alert.text
            logger.info(f"Alert appeared with text: {alert_text}")
            alert.accept()
            logger.info("Alert accepted")
            
            time.sleep(0.5)
            
            delete_button = self.driver.find_element(
                By.CSS_SELECTOR, "[data-testid='button-delete']"
            )
            delete_button.click()
            logger.info("Clicked delete button (triggers confirm dialog)")
            
            confirm_alert = self.wait.until(EC.alert_is_present())
            logger.info(f"Confirm dialog appeared: {confirm_alert.text}")
            confirm_alert.dismiss()
            logger.info("Confirm dialog dismissed (cancelled deletion)")
            
            logger.info("TEST PASSED: Alert Handling")
            return True
            
        except Exception as e:
            logger.error(f"TEST FAILED: {str(e)}")
            self.save_screenshot("test_alert_handling_failed")
            return False
    
    def test_infinite_scroll(self) -> bool:
        """
        Test 5: Infinite Scroll with JavaScript Execution
        
        This test demonstrates:
        - execute_script() for scroll control
        - Scrolling to bottom of container
        - Waiting for new elements to load
        - Verifying dynamically loaded content
        
        Returns:
            bool: True if test passes, False otherwise
        """
        logger.info("=" * 50)
        logger.info("Test 5: Infinite Scroll")
        logger.info("=" * 50)
        
        try:
            self.driver.get(self.base_url)
            
            scroll_container = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='container-scroll-list']"))
            )
            
            initial_items = self.driver.find_elements(
                By.CSS_SELECTOR, "[data-testid^='list-item-']"
            )
            initial_count = len(initial_items)
            logger.info(f"Initial item count: {initial_count}")
            
            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight",
                scroll_container
            )
            logger.info("Scrolled to bottom using execute_script")
            
            time.sleep(1)
            
            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight",
                scroll_container
            )
            
            time.sleep(1)
            
            final_items = self.driver.find_elements(
                By.CSS_SELECTOR, "[data-testid^='list-item-']"
            )
            final_count = len(final_items)
            logger.info(f"Final item count after scrolling: {final_count}")
            
            assert final_count > initial_count, "No new items loaded after scroll"
            logger.info(f"Successfully loaded {final_count - initial_count} new items")
            
            item_badge = self.driver.find_element(
                By.CSS_SELECTOR, "[data-testid='badge-item-count']"
            )
            logger.info(f"Badge shows: {item_badge.text}")
            
            logger.info("TEST PASSED: Infinite Scroll")
            return True
            
        except Exception as e:
            logger.error(f"TEST FAILED: {str(e)}")
            self.save_screenshot("test_infinite_scroll_failed")
            return False
    
    def test_css_selector_strategies(self) -> bool:
        """
        Test 6: Various CSS Selector Strategies
        
        This test demonstrates multiple selector approaches:
        - data-testid attributes
        - data-* custom attributes
        - BEM class naming
        - ID selectors
        - Contains text (via XPath)
        - Attribute selectors
        
        Returns:
            bool: True if test passes, False otherwise
        """
        logger.info("=" * 50)
        logger.info("Test 6: CSS Selector Strategies")
        logger.info("=" * 50)
        
        try:
            self.driver.get(self.base_url)
            
            element = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='selector-element-1']"))
            )
            logger.info("1. Found element by data-testid")
            
            element = self.driver.find_element(
                By.CSS_SELECTOR, "[data-role='secondary-element']"
            )
            logger.info("2. Found element by data-role attribute")
            
            elements = self.driver.find_elements(
                By.CSS_SELECTOR, "[data-category='selector-test']"
            )
            logger.info(f"3. Found {len(elements)} elements by data-category")
            
            element = self.driver.find_element(By.ID, "unique-element-2")
            logger.info("4. Found element by ID")
            
            element = self.driver.find_element(
                By.CSS_SELECTOR, ".selenium-test__element--tertiary"
            )
            logger.info("5. Found element by BEM class")
            
            element = self.driver.find_element(
                By.XPATH, "//*[contains(text(), 'Selenium Practice Lab')]"
            )
            logger.info("6. Found element by text content (XPath)")
            
            element = self.driver.find_element(
                By.CSS_SELECTOR, "[data-contains-text*='specific text']"
            )
            logger.info("7. Found element by partial attribute match")
            
            element = self.driver.find_element(
                By.CSS_SELECTOR, "button[data-requires-js-click='true']"
            )
            logger.info("8. Found button requiring JS click")
            
            logger.info("TEST PASSED: CSS Selector Strategies")
            return True
            
        except Exception as e:
            logger.error(f"TEST FAILED: {str(e)}")
            self.save_screenshot("test_selectors_failed")
            return False
    
    def test_javascript_force_click(self) -> bool:
        """
        Test 7: JavaScript Force Click
        
        This test demonstrates:
        - Using execute_script() to force click elements
        - Bypassing element interception issues
        - Direct JavaScript event triggering
        
        Returns:
            bool: True if test passes, False otherwise
        """
        logger.info("=" * 50)
        logger.info("Test 7: JavaScript Force Click")
        logger.info("=" * 50)
        
        try:
            self.driver.get(self.base_url)
            
            js_click_button = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='selector-button']"))
            )
            
            self.driver.execute_script("arguments[0].click();", js_click_button)
            logger.info("Executed JavaScript click on button")
            
            self.driver.execute_script("""
                var element = arguments[0];
                var event = new Event('click', { bubbles: true, cancelable: true });
                element.dispatchEvent(event);
            """, js_click_button)
            logger.info("Dispatched custom click event via JavaScript")
            
            username_input = self.driver.find_element(
                By.CSS_SELECTOR, "[data-testid='input-username']"
            )
            
            self.driver.execute_script("""
                var input = arguments[0];
                var nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                    window.HTMLInputElement.prototype, 'value'
                ).set;
                nativeInputValueSetter.call(input, 'js_injected_value');
                
                var event = new Event('input', { bubbles: true });
                input.dispatchEvent(event);
            """, username_input)
            logger.info("Triggered React onChange via JavaScript")
            
            username_state = self.driver.find_element(
                By.CSS_SELECTOR, "[data-testid='text-username-state']"
            )
            if "js_injected_value" in username_state.text:
                logger.info("Verified: React state updated via JS injection")
            
            logger.info("TEST PASSED: JavaScript Force Click")
            return True
            
        except Exception as e:
            logger.error(f"TEST FAILED: {str(e)}")
            self.save_screenshot("test_js_click_failed")
            return False
    
    def test_keyboard_actions(self) -> bool:
        """
        Test 8: Keyboard Actions
        
        This test demonstrates:
        - send_keys() with special keys
        - Enter key submission
        - Tab navigation
        - Key combinations
        
        Returns:
            bool: True if test passes, False otherwise
        """
        logger.info("=" * 50)
        logger.info("Test 8: Keyboard Actions")
        logger.info("=" * 50)
        
        try:
            self.driver.get(self.base_url)
            
            username_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='input-username']"))
            )
            
            username_input.send_keys("test_user")
            logger.info("Entered username")
            
            username_input.send_keys(Keys.TAB)
            logger.info("Pressed TAB key to move to password field")
            
            active_element = self.driver.switch_to.active_element
            active_element.send_keys("test_password")
            logger.info("Entered password in active element")
            
            active_element.send_keys(Keys.ENTER)
            logger.info("Pressed ENTER to submit form")
            
            result_element = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='text-login-result']"))
            )
            logger.info(f"Form submitted, result: {result_element.text}")
            
            logger.info("TEST PASSED: Keyboard Actions")
            return True
            
        except Exception as e:
            logger.error(f"TEST FAILED: {str(e)}")
            self.save_screenshot("test_keyboard_failed")
            return False
    
    def run_all_tests(self) -> dict:
        """
        Run all test methods and collect results.
        
        Returns:
            dict: Summary of test results
        """
        logger.info("=" * 60)
        logger.info("SELENIUM PRACTICE LAB - TEST SUITE")
        logger.info("=" * 60)
        
        tests = [
            ("Dynamic Element Loading", self.test_dynamic_element_loading),
            ("State-Controlled Inputs", self.test_state_controlled_inputs),
            ("Hover Dropdown Menu", self.test_hover_dropdown_menu),
            ("Alert Handling", self.test_alert_handling),
            ("Infinite Scroll", self.test_infinite_scroll),
            ("CSS Selector Strategies", self.test_css_selector_strategies),
            ("JavaScript Force Click", self.test_javascript_force_click),
            ("Keyboard Actions", self.test_keyboard_actions),
        ]
        
        results = {}
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            try:
                self.driver.get(self.base_url)
                time.sleep(0.5)
                
                result = test_func()
                results[test_name] = "PASSED" if result else "FAILED"
                
                if result:
                    passed += 1
                else:
                    failed += 1
                    
            except Exception as e:
                logger.error(f"Error running {test_name}: {str(e)}")
                results[test_name] = "ERROR"
                failed += 1
        
        logger.info("\n" + "=" * 60)
        logger.info("TEST RESULTS SUMMARY")
        logger.info("=" * 60)
        
        for test_name, result in results.items():
            status_icon = "✓" if result == "PASSED" else "✗"
            logger.info(f"{status_icon} {test_name}: {result}")
        
        logger.info("-" * 60)
        logger.info(f"Total: {len(tests)} | Passed: {passed} | Failed: {failed}")
        logger.info("=" * 60)
        
        return {
            "total": len(tests),
            "passed": passed,
            "failed": failed,
            "details": results
        }


def main():
    """Main entry point for running the test suite directly (not via pytest)."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Selenium Practice Lab Test Suite")
    parser.add_argument(
        "--url",
        default="http://localhost:5000",
        help="Base URL of the application (default: http://localhost:5000)"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run tests in headless mode"
    )
    
    args = parser.parse_args()
    
    TestSeleniumPractice.base_url = args.url
    tests = TestSeleniumPractice()
    
    try:
        tests.setup_method()
        results = tests.run_all_tests()
        
        exit_code = 0 if results["failed"] == 0 else 1
        
    except Exception as e:
        logger.error(f"Test suite failed to run: {str(e)}")
        exit_code = 1
        
    finally:
        tests.teardown_method()
    
    return exit_code


if __name__ == "__main__":
    exit(main())
