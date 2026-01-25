# Selenium Practice Lab - Test Scripts

React 기반 Selenium 실습 환경을 위한 Python 테스트 자동화 스크립트입니다.

## 설치 방법

```bash
# Python 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는 venv\Scripts\activate  # Windows

# 의존성 설치
pip install -r requirements.txt
```

## 실행 방법

```bash
# 기본 실행 (localhost:5000)
python test_selenium_practice.py

# 커스텀 URL로 실행
python test_selenium_practice.py --url http://your-app-url:port

# 헤드리스 모드 실행
python test_selenium_practice.py --headless
```

## 테스트 항목

### 1. Dynamic Element Loading (동적 요소 로딩)
- **목적**: Wait 전략 실습
- **기술**: WebDriverWait, expected_conditions
- **시나리오**: 버튼 클릭 후 2초 지연된 요소 대기

### 2. State-Controlled Inputs (State 제어 입력)
- **목적**: React 상태 관리 이해
- **기술**: send_keys(), onChange 이벤트 트리거
- **시나리오**: ID/PW 입력 및 상태 변경 확인

### 3. Hover Dropdown Menu (호버 드롭다운)
- **목적**: ActionChains 실습
- **기술**: move_to_element(), hover actions
- **시나리오**: 마우스 호버로 메뉴 표시 및 항목 클릭

### 4. Alert Handling (Alert 처리)
- **목적**: 브라우저 대화상자 제어
- **기술**: alert.accept(), alert.dismiss(), prompt 처리
- **시나리오**: confirm/alert 대화상자 응답

### 5. Infinite Scroll (무한 스크롤)
- **목적**: JavaScript 실행 실습
- **기술**: execute_script(), 스크롤 제어
- **시나리오**: 스크롤로 추가 항목 로드

### 6. CSS Selector Strategies (선택자 전략)
- **목적**: 다양한 요소 선택 방법
- **기술**: data-*, CSS 클래스, XPath
- **시나리오**: 여러 선택자로 요소 찾기

### 7. JavaScript Force Click (JS 강제 클릭)
- **목적**: 클릭 불가 요소 처리
- **기술**: execute_script() 직접 클릭
- **시나리오**: React 이벤트 강제 트리거

### 8. Keyboard Actions (키보드 액션)
- **목적**: 키보드 입력 제어
- **기술**: send_keys(), Keys.TAB, Keys.ENTER
- **시나리오**: 폼 네비게이션 및 제출

## 주요 기능 설명

### Wait 전략

```python
# Implicit Wait (전역 설정)
driver.implicitly_wait(5)

# Explicit Wait (특정 조건 대기)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='button']"))
)
```

### CSS Selector 활용

```python
# data-testid 선택
driver.find_element(By.CSS_SELECTOR, "[data-testid='button-login']")

# data-* 속성 선택
driver.find_element(By.CSS_SELECTOR, "[data-role='primary-element']")

# BEM 클래스 선택
driver.find_element(By.CSS_SELECTOR, ".selenium-test__element--primary")

# 복합 선택자
driver.find_element(By.CSS_SELECTOR, "button[data-action='submit']")
```

### ActionChains 활용

```python
from selenium.webdriver.common.action_chains import ActionChains

actions = ActionChains(driver)

# 마우스 호버
actions.move_to_element(element).perform()

# 더블 클릭
actions.double_click(element).perform()

# 드래그 앤 드롭
actions.drag_and_drop(source, target).perform()
```

### JavaScript 실행

```python
# 스크롤 제어
driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", container)

# 강제 클릭
driver.execute_script("arguments[0].click();", element)

# React 상태 변경 트리거
driver.execute_script("""
    var input = arguments[0];
    var nativeInputValueSetter = Object.getOwnPropertyDescriptor(
        window.HTMLInputElement.prototype, 'value'
    ).set;
    nativeInputValueSetter.call(input, 'new_value');
    input.dispatchEvent(new Event('input', { bubbles: true }));
""", input_element)
```

### 예외 처리 및 스크린샷

```python
try:
    # 테스트 실행
    element.click()
except Exception as e:
    # 실패 시 스크린샷 저장
    driver.save_screenshot(f"error_{timestamp}.png")
    logger.error(f"Test failed: {str(e)}")
```

## 폴더 구조

```
selenium_tests/
├── test_selenium_practice.py  # 메인 테스트 스크립트
├── requirements.txt           # Python 의존성
├── README.md                  # 이 문서
└── screenshots/               # 실패 시 스크린샷 저장
```

## 참고 사항

1. **Chrome WebDriver**: 최신 Chrome 브라우저와 호환되는 ChromeDriver가 필요합니다. webdriver-manager가 자동으로 관리합니다.

2. **React 특성**: React의 controlled component는 직접적인 DOM 조작이 불가능합니다. 반드시 `send_keys()`나 JavaScript 이벤트를 사용해야 합니다.

3. **Wait 전략**: React의 비동기 렌더링 때문에 적절한 Wait 전략이 필수입니다.

4. **스크린샷**: 테스트 실패 시 `screenshots/` 폴더에 자동으로 스크린샷이 저장됩니다.
