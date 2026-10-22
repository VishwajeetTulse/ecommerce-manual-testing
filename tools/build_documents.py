"""
build_documents.py - generates the test-case workbook and the Markdown
defect report from one Python data set, so the Excel sheet, the Markdown
files and the LaTeX report never disagree.

Run:  python tools/build_documents.py
Creates:
    test_cases/SwagLabs_Test_Cases.xlsx   (Test Cases, Defect Reports, RTM, Summary)
    docs/Test_Cases.md
    docs/Defect_Reports.md
"""
import os
from collections import Counter

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.saucedemo.com"
PWD = "secret_sauce"

# ---------------------------------------------------------------------------
# Test cases: (id, module, title, precondition, steps, test data, expected,
#              actual, status, priority, defect id, screenshot)
# ---------------------------------------------------------------------------
TC = [
    # ---------------- Login ----------------
    ("TC_LOGIN_01", "Login", "Verify login page elements are displayed",
     "Browser open", "1. Open " + SITE, "-",
     "Username field, Password field, Login button and Swag Labs logo are visible; accepted usernames are listed",
     "All elements displayed as expected", "Pass", "High", "", "01_login_page.png"),
    ("TC_LOGIN_02", "Login", "Verify placeholders of the input fields",
     "Login page open", "1. Observe Username and Password fields", "-",
     "Placeholders 'Username' and 'Password' are shown",
     "Placeholders shown correctly", "Pass", "Low", "", "01_login_page.png"),
    ("TC_LOGIN_03", "Login", "Login with valid credentials",
     "Login page open", "1. Enter username\n2. Enter password\n3. Click Login",
     "standard_user / " + PWD, "User is redirected to Products page (/inventory.html)",
     "Products page displayed", "Pass", "High", "", "05_inventory_standard_user.png"),
    ("TC_LOGIN_04", "Login", "Login with empty username and password",
     "Login page open", "1. Leave both fields empty\n2. Click Login", "blank / blank",
     "Error 'Epic sadface: Username is required' is shown",
     "Error message shown as expected", "Pass", "High", "", "02_login_empty_fields_error.png"),
    ("TC_LOGIN_05", "Login", "Login with valid username and wrong password",
     "Login page open", "1. Enter username\n2. Enter wrong password\n3. Click Login",
     "standard_user / wrong", "Error 'Username and password do not match any user in this service'",
     "Error message shown as expected", "Pass", "High", "", "04_wrong_password_error.png"),
    ("TC_LOGIN_06", "Login", "Login with locked-out user",
     "Login page open", "1. Enter username\n2. Enter password\n3. Click Login",
     "locked_out_user / " + PWD, "Error 'Sorry, this user has been locked out.' is shown",
     "Error message shown as expected", "Pass", "High", "", "03_locked_out_user_error.png"),
    ("TC_LOGIN_07", "Login", "Password field masks the typed characters",
     "Login page open", "1. Type text in Password field", "secret_sauce",
     "Characters are shown as dots", "Characters masked", "Pass", "Medium", "", "01_login_page.png"),
    ("TC_LOGIN_08", "Login", "Login response time for performance_glitch_user",
     "Login page open", "1. Enter username\n2. Enter password\n3. Click Login and time it",
     "performance_glitch_user / " + PWD, "Products page loads within 3 seconds",
     "Products page took about 7 seconds to load", "Fail", "Medium", "DEF-08", "20_performance_glitch_user.png"),

    # ---------------- Products ----------------
    ("TC_PROD_01", "Products", "Verify six products are listed with name, image, description and price",
     "Logged in as standard_user", "1. Observe Products page", "-",
     "6 products displayed, each with a unique image, name, description and price",
     "6 products displayed correctly", "Pass", "High", "", "05_inventory_standard_user.png"),
    ("TC_PROD_02", "Products", "Sort products by price low to high",
     "Logged in as standard_user", "1. Select 'Price (low to high)' in sort dropdown", "lohi",
     "Products ordered 7.99, 9.99, 15.99, 15.99, 29.99, 49.99",
     "Order 7.99, 9.99, 15.99, 15.99, 29.99, 49.99", "Pass", "Medium", "", "06_sort_price_low_high.png"),
    ("TC_PROD_03", "Products", "Sort products by name Z to A",
     "Logged in as standard_user", "1. Select 'Name (Z to A)'", "za",
     "Products listed in reverse alphabetical order", "Reverse alphabetical order shown", "Pass", "Medium", "", ""),
    ("TC_PROD_04", "Products", "Product images match the product (problem_user)",
     "Logged in as problem_user", "1. Observe product images", "problem_user / " + PWD,
     "Each product shows its own image", "Every product shows the same dog image", "Fail", "High", "DEF-01", "15_problem_user_same_images.png"),
    ("TC_PROD_05", "Products", "Sort by price works for problem_user",
     "Logged in as problem_user", "1. Select 'Price (low to high)'", "lohi",
     "Products reordered by ascending price", "Order unchanged: 29.99, 9.99, 15.99, 49.99, 7.99, 15.99", "Fail", "Medium", "DEF-02", "16_problem_user_sort_broken.png"),
    ("TC_PROD_06", "Products", "Sort dropdown works for error_user",
     "Logged in as error_user", "1. Select 'Name (Z to A)'", "za",
     "Products reordered", "JavaScript alert 'Sorting is broken! This error has been reported to Backtrace.'", "Fail", "Medium", "DEF-07", "19_error_user_sort_alert.png"),
    ("TC_PROD_07", "Products", "Prices shown for visual_user match the catalogue",
     "Logged in as visual_user", "1. Compare prices with standard_user prices", "visual_user / " + PWD,
     "Backpack $29.99, Bike Light $9.99, Bolt T-Shirt $15.99, Fleece Jacket $49.99",
     "Backpack $69.96, Bike Light $91.76, Bolt T-Shirt $14.41, Fleece Jacket $47.3", "Fail", "High", "DEF-09", "21_visual_user_layout.png"),
    ("TC_PROD_08", "Products", "Layout of Products page for visual_user",
     "Logged in as visual_user", "1. Observe header and product cards", "-",
     "Cart icon aligned in header; product names left-aligned",
     "Cart icon shifted below header line; some product names shifted right", "Fail", "Low", "DEF-09", "21_visual_user_layout.png"),

    # ---------------- Cart ----------------
    ("TC_CART_01", "Cart", "Add two products to cart and verify badge",
     "Logged in as standard_user", "1. Click Add to cart on Backpack\n2. Click Add to cart on Bike Light", "-",
     "Cart badge shows 2; buttons change to 'Remove'", "Badge shows 2, buttons show Remove", "Pass", "High", "", "07_items_added_badge.png"),
    ("TC_CART_02", "Cart", "Cart page lists the added products with correct prices",
     "Two items in cart", "1. Click cart icon", "-",
     "Backpack $29.99 and Bike Light $9.99 listed with QTY 1 each", "Both items listed correctly", "Pass", "High", "", "08_cart_page.png"),
    ("TC_CART_03", "Cart", "Remove a product from the cart page",
     "Two items in cart", "1. Click Remove on Bike Light", "-",
     "Item removed; badge shows 1", "Item removed, badge shows 1", "Pass", "Medium", "", ""),
    ("TC_CART_04", "Cart", "Add to cart works for all products (problem_user)",
     "Logged in as problem_user", "1. Click Add to cart on Fleece Jacket\n2. Click Add to cart on T-Shirt (Red)", "-",
     "Badge shows 2", "No badge appears; buttons do not change to Remove", "Fail", "High", "DEF-03", "17_problem_user_add_to_cart_fails.png"),
    ("TC_CART_05", "Cart", "Cart is cleared on logout",
     "Logged in as standard_user, Onesie in cart", "1. Logout from side menu\n2. Login again as standard_user", "-",
     "Cart is empty after a fresh login", "Cart badge still shows 1 after re-login", "Fail", "Medium", "DEF-06", "14_cart_persists_after_relogin.png"),
    ("TC_CART_06", "Cart", "Continue Shopping returns to Products page",
     "Cart page open", "1. Click Continue Shopping", "-",
     "Products page displayed", "Products page displayed", "Pass", "Low", "", ""),

    # ---------------- Checkout ----------------
    ("TC_CHK_01", "Checkout", "Checkout with empty information form",
     "Cart has items; on Checkout: Your Information", "1. Click Continue without entering data", "blank",
     "Error 'First Name is required'", "Error shown as expected", "Pass", "High", "", "09_checkout_empty_form_error.png"),
    ("TC_CHK_02", "Checkout", "Checkout with first name only",
     "On Checkout: Your Information", "1. Enter first name\n2. Click Continue", "Vishwajeet",
     "Error 'Last Name is required'", "Error shown as expected", "Pass", "High", "", ""),
    ("TC_CHK_03", "Checkout", "Checkout with first and last name only",
     "On Checkout: Your Information", "1. Enter first and last name\n2. Click Continue", "Vishwajeet / Tulse",
     "Error 'Postal Code is required'", "Error shown as expected", "Pass", "High", "", ""),
    ("TC_CHK_04", "Checkout", "Checkout with valid information",
     "On Checkout: Your Information", "1. Enter all fields\n2. Click Continue", "Vishwajeet / Tulse / 411041",
     "Checkout: Overview page displayed", "Overview displayed", "Pass", "High", "", "11_checkout_overview.png"),
    ("TC_CHK_05", "Checkout", "First name rejects numeric input",
     "On Checkout: Your Information", "1. Enter digits in First Name\n2. Fill other fields\n3. Continue", "12345 / Tulse / 411041",
     "Validation error for First Name", "Form accepted and Overview displayed", "Fail", "Medium", "DEF-05", "10_checkout_invalid_data_accepted.png"),
    ("TC_CHK_06", "Checkout", "Postal code rejects alphabetic input",
     "On Checkout: Your Information", "1. Enter letters in Postal Code\n2. Continue", "Vishwajeet / Tulse / abc",
     "Validation error for Postal Code", "Form accepted and Overview displayed", "Fail", "Medium", "DEF-05", "10_checkout_invalid_data_accepted.png"),
    ("TC_CHK_07", "Checkout", "Overview shows correct item total, tax and total",
     "Backpack and Bike Light in cart; on Overview", "1. Read Price Total section", "-",
     "Item total $39.98, Tax $3.20 (8%), Total $43.18", "Item total $39.98, Tax $3.20, Total $43.18", "Pass", "High", "", "11_checkout_overview.png"),
    ("TC_CHK_08", "Checkout", "Overview shows payment and shipping information",
     "On Overview", "1. Read Payment and Shipping sections", "-",
     "Payment 'SauceCard #31337' and shipping 'Free Pony Express Delivery!' shown", "Shown as expected", "Pass", "Low", "", "11_checkout_overview.png"),
    ("TC_CHK_09", "Checkout", "Finish order shows confirmation",
     "On Overview", "1. Click Finish", "-",
     "'Thank you for your order!' page with Back Home button", "Confirmation shown; cart badge cleared", "Pass", "High", "", "12_order_complete.png"),
    ("TC_CHK_10", "Checkout", "Last Name field accepts input for problem_user",
     "Logged in as problem_user; on Your Information", "1. Type in First Name\n2. Type in Last Name\n3. Type postal code\n4. Continue",
     "Vishwajeet / Tulse / 411041", "Overview displayed",
     "Keystrokes typed in Last Name replace First Name; Last Name stays empty; error 'Last Name is required'", "Fail", "Critical", "DEF-04", "18_problem_user_lastname_bug.png"),
    ("TC_CHK_11", "Checkout", "Cancel on Your Information returns to cart",
     "On Your Information", "1. Click Cancel", "-", "Cart page displayed", "Cart page displayed", "Pass", "Low", "", ""),

    # ---------------- Menu / navigation ----------------
    ("TC_MENU_01", "Menu", "Side menu opens with all navigation links",
     "Logged in", "1. Click hamburger icon", "-",
     "All Items, Dynamic Catalog, About, Logout, Reset App State links shown", "All five links shown", "Pass", "Medium", "", "13_side_menu.png"),
    ("TC_MENU_02", "Menu", "Logout returns to login page",
     "Side menu open", "1. Click Logout", "-",
     "Login page displayed (" + SITE + "/)", "Login page displayed", "Pass", "High", "", ""),
    ("TC_MENU_03", "Menu", "Protected page cannot be opened without login",
     "Logged out", "1. Open " + SITE + "/inventory.html directly", "-",
     "Redirected to login with error 'You can only access /inventory.html when you are logged in.'",
     "Redirected with the expected error", "Pass", "High", "", ""),

    # ---------------- UI ----------------
    ("TC_UI_01", "UI", "Cart badge count equals number of items",
     "Logged in as standard_user", "1. Add 1, then 2 items", "-",
     "Badge shows 1 then 2", "Badge updates correctly", "Pass", "Medium", "", "07_items_added_badge.png"),
    ("TC_UI_02", "UI", "Add to cart button toggles to Remove",
     "Logged in as standard_user", "1. Click Add to cart on any product", "-",
     "Button label changes to Remove", "Label changes to Remove", "Pass", "Low", "", "07_items_added_badge.png"),
    ("TC_UI_03", "UI", "Footer shows social links and copyright",
     "Logged in", "1. Scroll to page bottom", "-",
     "Twitter, Facebook, LinkedIn icons and copyright text visible", "Visible as expected", "Pass", "Low", "", "18_problem_user_lastname_bug.png"),
]

# ---------------------------------------------------------------------------
# Defect reports
# ---------------------------------------------------------------------------
DEF = [
    ("DEF-01", "Wrong product images for problem_user", "Products", "High", "Medium", "Open",
     "1. Login as problem_user\n2. Observe the Products page",
     "Each product shows its own image", "All six products show the same dog image",
     "TC_PROD_04", "15_problem_user_same_images.png"),
    ("DEF-02", "Price sorting does not reorder products for problem_user", "Products", "Medium", "Medium", "Open",
     "1. Login as problem_user\n2. Select 'Price (low to high)'",
     "Products reordered 7.99 ... 49.99", "Order stays 29.99, 9.99, 15.99, 49.99, 7.99, 15.99",
     "TC_PROD_05", "16_problem_user_sort_broken.png"),
    ("DEF-03", "Add to cart has no effect for some products (problem_user)", "Cart", "High", "High", "Open",
     "1. Login as problem_user\n2. Click Add to cart on Fleece Jacket and T-Shirt (Red)",
     "Badge shows 2 and buttons change to Remove", "Nothing happens; no badge, buttons unchanged",
     "TC_CART_04", "17_problem_user_add_to_cart_fails.png"),
    ("DEF-04", "Last Name field cannot be filled during checkout (problem_user)", "Checkout", "Critical", "High", "Open",
     "1. Login as problem_user, add an item, go to Checkout\n2. Type in First Name, then Last Name, then Postal Code\n3. Click Continue",
     "Overview page displayed", "Text typed into Last Name replaces First Name; Last Name stays empty; 'Error: Last Name is required'. Checkout is blocked.",
     "TC_CHK_10", "18_problem_user_lastname_bug.png"),
    ("DEF-05", "Checkout form accepts invalid data (all users)", "Checkout", "Medium", "Medium", "Open",
     "1. Login as standard_user, add an item, go to Checkout\n2. Enter First Name 12345, Last Name !!!, Postal Code abc\n3. Click Continue",
     "Validation errors for name and postal code", "Form accepted; Overview page displayed",
     "TC_CHK_05, TC_CHK_06", "10_checkout_invalid_data_accepted.png"),
    ("DEF-06", "Cart contents persist after logout and re-login", "Cart", "Medium", "Low", "Open",
     "1. Login as standard_user, add Onesie\n2. Logout\n3. Login again as standard_user",
     "Cart is empty after fresh login", "Badge shows 1; Onesie still in cart",
     "TC_CART_05", "14_cart_persists_after_relogin.png"),
    ("DEF-07", "Sorting shows a JavaScript alert for error_user", "Products", "Medium", "Medium", "Open",
     "1. Login as error_user\n2. Select 'Name (Z to A)'",
     "Products reordered", "Alert 'Sorting is broken! This error has been reported to Backtrace.'",
     "TC_PROD_06", "19_error_user_sort_alert.png"),
    ("DEF-08", "Login takes about 7 seconds for performance_glitch_user", "Login", "Medium", "Low", "Open",
     "1. Login as performance_glitch_user and measure time to Products page",
     "Page loads within 3 seconds", "About 6.8 seconds",
     "TC_LOGIN_08", "20_performance_glitch_user.png"),
    ("DEF-09", "Wrong prices and misaligned layout for visual_user", "Products", "High", "Medium", "Open",
     "1. Login as visual_user\n2. Compare prices and layout with standard_user",
     "Backpack $29.99, Bike Light $9.99; cart icon aligned in header",
     "Backpack $69.96, Bike Light $91.76, Bolt T-Shirt $14.41, Fleece Jacket $47.3; cart icon drops below header; titles shifted",
     "TC_PROD_07, TC_PROD_08", "21_visual_user_layout.png"),
]

# Requirement traceability
REQ = [
    ("REQ-01", "User can log in with valid credentials and is blocked otherwise", "TC_LOGIN_01 - TC_LOGIN_08, TC_MENU_03"),
    ("REQ-02", "Products are listed with correct details and can be sorted", "TC_PROD_01 - TC_PROD_08"),
    ("REQ-03", "User can add and remove products in the cart", "TC_CART_01 - TC_CART_06, TC_UI_01, TC_UI_02"),
    ("REQ-04", "Checkout validates customer information", "TC_CHK_01 - TC_CHK_06, TC_CHK_10, TC_CHK_11"),
    ("REQ-05", "Order overview shows correct totals and order can be completed", "TC_CHK_07 - TC_CHK_09"),
    ("REQ-06", "Navigation menu and logout work", "TC_MENU_01 - TC_MENU_03, TC_UI_03"),
]

HEAD_FILL = PatternFill("solid", fgColor="1F4E78")
HEAD_FONT = Font(bold=True, color="FFFFFF")
PASS_FILL = PatternFill("solid", fgColor="C6EFCE")
FAIL_FILL = PatternFill("solid", fgColor="FFC7CE")
THIN = Side(style="thin", color="999999")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")


def write_sheet(ws, headers, rows, widths, status_col=None):
    ws.append(headers)
    for c in ws[1]:
        c.fill, c.font, c.border, c.alignment = HEAD_FILL, HEAD_FONT, BORDER, Alignment(wrap_text=True, vertical="center")
    for r in rows:
        ws.append(list(r))
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.border, c.alignment = BORDER, WRAP
        if status_col is not None:
            s = row[status_col]
            if s.value == "Pass":
                s.fill = PASS_FILL
            elif s.value == "Fail":
                s.fill = FAIL_FILL
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"


def build_excel(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Test Cases"
    write_sheet(ws,
                ["Test Case ID", "Module", "Title", "Pre-condition", "Test Steps", "Test Data",
                 "Expected Result", "Actual Result", "Status", "Priority", "Defect ID", "Evidence"],
                TC, [14, 11, 34, 26, 36, 24, 40, 40, 8, 9, 10, 30], status_col=8)

    ws = wb.create_sheet("Defect Reports")
    write_sheet(ws,
                ["Defect ID", "Summary", "Module", "Severity", "Priority", "Status",
                 "Steps to Reproduce", "Expected Result", "Actual Result", "Test Case", "Evidence"],
                DEF, [10, 40, 11, 10, 10, 9, 40, 36, 44, 16, 30])

    ws = wb.create_sheet("RTM")
    write_sheet(ws, ["Requirement ID", "Requirement", "Test Cases"], REQ, [15, 60, 50])

    ws = wb.create_sheet("Summary")
    status = Counter(t[8] for t in TC)
    mods = sorted({t[1] for t in TC}, key=lambda m: [t[1] for t in TC].index(m))
    rows = [("Application under test", "Swag Labs (" + SITE + ")"),
            ("Testing type", "Manual functional, UI and negative testing"),
            ("Browser", "Microsoft Edge 142 (Windows 11)"),
            ("Total test cases", len(TC)),
            ("Passed", status["Pass"]),
            ("Failed", status["Fail"]),
            ("Pass percentage", f"{100 * status['Pass'] / len(TC):.1f}%"),
            ("Defects logged", len(DEF)),
            ("Critical / High / Medium / Low defects",
             " / ".join(str(sum(1 for d in DEF if d[3] == s)) for s in ("Critical", "High", "Medium", "Low"))),
            ("", "")]
    for m in mods:
        sub = [t for t in TC if t[1] == m]
        rows.append((f"{m}: total / pass / fail",
                     f"{len(sub)} / {sum(1 for t in sub if t[8] == 'Pass')} / {sum(1 for t in sub if t[8] == 'Fail')}"))
    write_sheet(ws, ["Metric", "Value"], rows, [40, 60])
    wb.save(path)
    return status


def build_markdown(status):
    lines = ["# Test Cases - Swag Labs manual testing", "",
             f"Total: {len(TC)} | Pass: {status['Pass']} | Fail: {status['Fail']}", "",
             "| ID | Module | Title | Test data | Expected | Actual | Status | Defect |",
             "|---|---|---|---|---|---|---|---|"]
    for t in TC:
        lines.append(f"| {t[0]} | {t[1]} | {t[2]} | {t[5]} | {t[6]} | {t[7]} | {t[8]} | {t[10]} |")
    with open(os.path.join(ROOT, "docs", "Test_Cases.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    lines = ["# Defect Reports - Swag Labs manual testing", "",
             f"{len(DEF)} defects were logged. Severity: how badly the defect affects the user. "
             "Priority: how soon it should be fixed.", ""]
    for d in DEF:
        lines += [f"## {d[0]}: {d[1]}", "",
                  f"- **Module:** {d[2]}", f"- **Severity:** {d[3]}", f"- **Priority:** {d[4]}", f"- **Status:** {d[5]}",
                  f"- **Environment:** Microsoft Edge 142, Windows 11, {SITE}",
                  f"- **Linked test case:** {d[9]}", "", "**Steps to reproduce**", ""]
        lines += [f"{s}" for s in d[6].split("\n")]
        lines += ["", f"**Expected result:** {d[7]}", "", f"**Actual result:** {d[8]}", "",
                  f"**Evidence:** `screenshots/{d[10]}`", "", f"![{d[0]}](../screenshots/{d[10]})", ""]
    with open(os.path.join(ROOT, "docs", "Defect_Reports.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    os.makedirs(os.path.join(ROOT, "test_cases"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "docs"), exist_ok=True)
    xlsx = os.path.join(ROOT, "test_cases", "SwagLabs_Test_Cases.xlsx")
    status = build_excel(xlsx)
    build_markdown(status)
    print(f"{len(TC)} test cases ({status['Pass']} pass, {status['Fail']} fail), {len(DEF)} defects")
    print("written:", xlsx, "docs/Test_Cases.md, docs/Defect_Reports.md")


if __name__ == "__main__":
    main()
