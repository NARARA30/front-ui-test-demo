# Selenium Practice Lab

A React-based practice environment for learning Selenium test automation.

## Overview

This project provides a comprehensive training environment for learning Selenium WebDriver automation with React applications. It includes dynamic UI elements, state-controlled forms, hover menus, alert dialogs, and infinite scroll functionality - all designed to practice real-world test automation scenarios.

## Project Structure

```
├── client/                     # React Frontend
│   ├── src/
│   │   ├── pages/
│   │   │   └── home.tsx        # Main practice page with all test elements
│   │   ├── components/ui/      # Shadcn UI components
│   │   ├── index.css           # Design tokens and styling
│   │   └── App.tsx             # App routing
│   └── index.html
├── server/                     # Express Backend
│   ├── routes.ts               # API endpoints
│   └── storage.ts              # In-memory storage
├── shared/
│   └── schema.ts               # TypeScript types and Zod schemas
├── selenium_tests/             # Python Selenium test scripts
│   ├── test_selenium_practice.py
│   ├── requirements.txt
│   └── README.md
└── replit.md                   # This file
```

## Features for Selenium Practice

### 1. Dynamic Element Loading
- Button triggers 2-second delayed element rendering
- Practice for WebDriverWait and expected_conditions

### 2. State-Controlled Login Form
- React controlled inputs (onChange handlers)
- Demonstrates why direct DOM manipulation fails

### 3. Hover Dropdown Menu
- ActionChains practice with move_to_element()
- Menu only visible on hover

### 4. Alert Dialog Testing
- Browser alert(), confirm(), and prompt() dialogs
- Practice alert handling with Selenium

### 5. Infinite Scroll List
- execute_script() for scroll control
- Dynamic content loading on scroll

### 6. CSS Selector Practice
- data-testid attributes
- Custom data-* attributes
- BEM class naming conventions
- Complex selector structures

## Running the Application

The application runs on port 5000:
```bash
npm run dev
```

## Running Selenium Tests

```bash
cd selenium_tests
pip install -r requirements.txt
python test_selenium_practice.py --url http://localhost:5000
```

## Tech Stack

- **Frontend**: React, TypeScript, Tailwind CSS, Shadcn UI
- **Backend**: Express.js, TypeScript
- **Test Automation**: Python, Selenium WebDriver

## Key Test Automation Concepts

1. **Wait Strategies**: Implicit vs Explicit waits
2. **Selector Strategies**: CSS, XPath, data attributes
3. **ActionChains**: Mouse hover, click, double-click
4. **JavaScript Execution**: Scroll control, force click
5. **Alert Handling**: Accept, dismiss, send_keys to prompts
6. **Exception Handling**: Screenshot on failure
