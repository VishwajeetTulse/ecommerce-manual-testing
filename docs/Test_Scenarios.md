# Test Scenarios - Swag Labs

A test scenario is a one-line statement of *what* to test. Each scenario is
expanded into one or more test cases in `test_cases/SwagLabs_Test_Cases.xlsx`.

## Login

| ID | Scenario | Test cases |
|---|---|---|
| TS_01 | Verify login page UI elements and placeholders | TC_LOGIN_01, TC_LOGIN_02, TC_LOGIN_07 |
| TS_02 | Verify login with valid credentials | TC_LOGIN_03 |
| TS_03 | Verify login with empty, wrong and locked-out credentials | TC_LOGIN_04, TC_LOGIN_05, TC_LOGIN_06 |
| TS_04 | Verify login response time | TC_LOGIN_08 |
| TS_05 | Verify protected pages cannot be opened without login | TC_MENU_03 |

## Products

| ID | Scenario | Test cases |
|---|---|---|
| TS_06 | Verify product listing shows name, image, description and price | TC_PROD_01 |
| TS_07 | Verify sorting by name and price | TC_PROD_02, TC_PROD_03, TC_PROD_05, TC_PROD_06 |
| TS_08 | Verify product data is correct for every test user | TC_PROD_04, TC_PROD_07, TC_PROD_08 |

## Cart

| ID | Scenario | Test cases |
|---|---|---|
| TS_09 | Verify adding products updates the cart badge and button state | TC_CART_01, TC_UI_01, TC_UI_02 |
| TS_10 | Verify cart page contents and removal | TC_CART_02, TC_CART_03, TC_CART_06 |
| TS_11 | Verify add to cart for the problem user | TC_CART_04 |
| TS_12 | Verify cart state after logout | TC_CART_05 |

## Checkout

| ID | Scenario | Test cases |
|---|---|---|
| TS_13 | Verify mandatory field validation on the information form | TC_CHK_01, TC_CHK_02, TC_CHK_03 |
| TS_14 | Verify data-type validation of name and postal code | TC_CHK_05, TC_CHK_06 |
| TS_15 | Verify successful checkout and order confirmation | TC_CHK_04, TC_CHK_09 |
| TS_16 | Verify overview totals, tax and payment information | TC_CHK_07, TC_CHK_08 |
| TS_17 | Verify checkout form for the problem user | TC_CHK_10 |
| TS_18 | Verify cancel navigation | TC_CHK_11 |

## Menu and UI

| ID | Scenario | Test cases |
|---|---|---|
| TS_19 | Verify side menu links and logout | TC_MENU_01, TC_MENU_02 |
| TS_20 | Verify footer content | TC_UI_03 |
