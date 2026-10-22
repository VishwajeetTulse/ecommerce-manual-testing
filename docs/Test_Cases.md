# Test Cases - Swag Labs manual testing

Total: 39 | Pass: 28 | Fail: 11

| ID | Module | Title | Test data | Expected | Actual | Status | Defect |
|---|---|---|---|---|---|---|---|
| TC_LOGIN_01 | Login | Verify login page elements are displayed | - | Username field, Password field, Login button and Swag Labs logo are visible; accepted usernames are listed | All elements displayed as expected | Pass |  |
| TC_LOGIN_02 | Login | Verify placeholders of the input fields | - | Placeholders 'Username' and 'Password' are shown | Placeholders shown correctly | Pass |  |
| TC_LOGIN_03 | Login | Login with valid credentials | standard_user / secret_sauce | User is redirected to Products page (/inventory.html) | Products page displayed | Pass |  |
| TC_LOGIN_04 | Login | Login with empty username and password | blank / blank | Error 'Epic sadface: Username is required' is shown | Error message shown as expected | Pass |  |
| TC_LOGIN_05 | Login | Login with valid username and wrong password | standard_user / wrong | Error 'Username and password do not match any user in this service' | Error message shown as expected | Pass |  |
| TC_LOGIN_06 | Login | Login with locked-out user | locked_out_user / secret_sauce | Error 'Sorry, this user has been locked out.' is shown | Error message shown as expected | Pass |  |
| TC_LOGIN_07 | Login | Password field masks the typed characters | secret_sauce | Characters are shown as dots | Characters masked | Pass |  |
| TC_LOGIN_08 | Login | Login response time for performance_glitch_user | performance_glitch_user / secret_sauce | Products page loads within 3 seconds | Products page took about 7 seconds to load | Fail | DEF-08 |
| TC_PROD_01 | Products | Verify six products are listed with name, image, description and price | - | 6 products displayed, each with a unique image, name, description and price | 6 products displayed correctly | Pass |  |
| TC_PROD_02 | Products | Sort products by price low to high | lohi | Products ordered 7.99, 9.99, 15.99, 15.99, 29.99, 49.99 | Order 7.99, 9.99, 15.99, 15.99, 29.99, 49.99 | Pass |  |
| TC_PROD_03 | Products | Sort products by name Z to A | za | Products listed in reverse alphabetical order | Reverse alphabetical order shown | Pass |  |
| TC_PROD_04 | Products | Product images match the product (problem_user) | problem_user / secret_sauce | Each product shows its own image | Every product shows the same dog image | Fail | DEF-01 |
| TC_PROD_05 | Products | Sort by price works for problem_user | lohi | Products reordered by ascending price | Order unchanged: 29.99, 9.99, 15.99, 49.99, 7.99, 15.99 | Fail | DEF-02 |
| TC_PROD_06 | Products | Sort dropdown works for error_user | za | Products reordered | JavaScript alert 'Sorting is broken! This error has been reported to Backtrace.' | Fail | DEF-07 |
| TC_PROD_07 | Products | Prices shown for visual_user match the catalogue | visual_user / secret_sauce | Backpack $29.99, Bike Light $9.99, Bolt T-Shirt $15.99, Fleece Jacket $49.99 | Backpack $69.96, Bike Light $91.76, Bolt T-Shirt $14.41, Fleece Jacket $47.3 | Fail | DEF-09 |
| TC_PROD_08 | Products | Layout of Products page for visual_user | - | Cart icon aligned in header; product names left-aligned | Cart icon shifted below header line; some product names shifted right | Fail | DEF-09 |
| TC_CART_01 | Cart | Add two products to cart and verify badge | - | Cart badge shows 2; buttons change to 'Remove' | Badge shows 2, buttons show Remove | Pass |  |
| TC_CART_02 | Cart | Cart page lists the added products with correct prices | - | Backpack $29.99 and Bike Light $9.99 listed with QTY 1 each | Both items listed correctly | Pass |  |
| TC_CART_03 | Cart | Remove a product from the cart page | - | Item removed; badge shows 1 | Item removed, badge shows 1 | Pass |  |
| TC_CART_04 | Cart | Add to cart works for all products (problem_user) | - | Badge shows 2 | No badge appears; buttons do not change to Remove | Fail | DEF-03 |
| TC_CART_05 | Cart | Cart is cleared on logout | - | Cart is empty after a fresh login | Cart badge still shows 1 after re-login | Fail | DEF-06 |
| TC_CART_06 | Cart | Continue Shopping returns to Products page | - | Products page displayed | Products page displayed | Pass |  |
| TC_CHK_01 | Checkout | Checkout with empty information form | blank | Error 'First Name is required' | Error shown as expected | Pass |  |
| TC_CHK_02 | Checkout | Checkout with first name only | Vishwajeet | Error 'Last Name is required' | Error shown as expected | Pass |  |
| TC_CHK_03 | Checkout | Checkout with first and last name only | Vishwajeet / Tulse | Error 'Postal Code is required' | Error shown as expected | Pass |  |
| TC_CHK_04 | Checkout | Checkout with valid information | Vishwajeet / Tulse / 411041 | Checkout: Overview page displayed | Overview displayed | Pass |  |
| TC_CHK_05 | Checkout | First name rejects numeric input | 12345 / Tulse / 411041 | Validation error for First Name | Form accepted and Overview displayed | Fail | DEF-05 |
| TC_CHK_06 | Checkout | Postal code rejects alphabetic input | Vishwajeet / Tulse / abc | Validation error for Postal Code | Form accepted and Overview displayed | Fail | DEF-05 |
| TC_CHK_07 | Checkout | Overview shows correct item total, tax and total | - | Item total $39.98, Tax $3.20 (8%), Total $43.18 | Item total $39.98, Tax $3.20, Total $43.18 | Pass |  |
| TC_CHK_08 | Checkout | Overview shows payment and shipping information | - | Payment 'SauceCard #31337' and shipping 'Free Pony Express Delivery!' shown | Shown as expected | Pass |  |
| TC_CHK_09 | Checkout | Finish order shows confirmation | - | 'Thank you for your order!' page with Back Home button | Confirmation shown; cart badge cleared | Pass |  |
| TC_CHK_10 | Checkout | Last Name field accepts input for problem_user | Vishwajeet / Tulse / 411041 | Overview displayed | Keystrokes typed in Last Name replace First Name; Last Name stays empty; error 'Last Name is required' | Fail | DEF-04 |
| TC_CHK_11 | Checkout | Cancel on Your Information returns to cart | - | Cart page displayed | Cart page displayed | Pass |  |
| TC_MENU_01 | Menu | Side menu opens with all navigation links | - | All Items, Dynamic Catalog, About, Logout, Reset App State links shown | All five links shown | Pass |  |
| TC_MENU_02 | Menu | Logout returns to login page | - | Login page displayed (https://www.saucedemo.com/) | Login page displayed | Pass |  |
| TC_MENU_03 | Menu | Protected page cannot be opened without login | - | Redirected to login with error 'You can only access /inventory.html when you are logged in.' | Redirected with the expected error | Pass |  |
| TC_UI_01 | UI | Cart badge count equals number of items | - | Badge shows 1 then 2 | Badge updates correctly | Pass |  |
| TC_UI_02 | UI | Add to cart button toggles to Remove | - | Button label changes to Remove | Label changes to Remove | Pass |  |
| TC_UI_03 | UI | Footer shows social links and copyright | - | Twitter, Facebook, LinkedIn icons and copyright text visible | Visible as expected | Pass |  |
