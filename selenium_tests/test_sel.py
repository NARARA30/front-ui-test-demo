import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




BASE_URL = "https://react-selenium-automation.replit.app/"

@pytest.fixture
def driver():
    
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def test_buttun_click_and_input(driver):
    wait = WebDriverWait(driver, 10)
    driver.get(BASE_URL)

    btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="button-load-elements"]')))
    btn.click()
    print("\n[SUCCESS] 버튼 클릭에 성공했습니다!")

    text_value = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="input-dynamic"]')))
    text_value.send_keys("테스트 중입니다")
    print("[SUCCESS] 입력창에 텍스트를 입력했습니다.")