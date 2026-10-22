"""
capture_evidence.py - takes the screenshots used as evidence in the manual
test cases and defect reports for the Swag Labs demo e-commerce site
(https://www.saucedemo.com).

The manual test cases were executed by hand in a browser. This script only
re-creates the key screens so that the evidence in the repository is
reproducible. It also prints a few observations that were used to confirm
the defects (sorting, product images, checkout validation).

Run:  python tools/capture_evidence.py
Needs: pip install selenium   (Microsoft Edge or Chrome installed)
"""
import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

URL = "https://www.saucedemo.com/"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "screenshots")
PASSWORD = "secret_sauce"


def make_driver():
    for name in ("Edge", "Chrome"):
        try:
            opts = getattr(webdriver, f"{name}Options")()
            opts.add_argument("--headless=new")
            opts.add_argument("--window-size=1280,900")
            return getattr(webdriver, name)(options=opts)
        except Exception as exc:  # try the next browser
            print(f"{name} not available: {exc.__class__.__name__}")
    sys.exit("No supported browser found")


def shot(driver, name):
    path = os.path.join(OUT, name + ".png")
    driver.save_screenshot(path)
    print(f"  saved {path}")


def login(driver, user, password=PASSWORD):
    driver.get(URL)
    driver.find_element(By.ID, "user-name").clear()
    driver.find_element(By.ID, "user-name").send_keys(user)
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(1)


def main():
    os.makedirs(OUT, exist_ok=True)
    d = make_driver()
    d.implicitly_wait(5)

    print("[1] Login page and negative login")
    d.get(URL)
    shot(d, "01_login_page")
    login(d, "", "")
    shot(d, "02_login_empty_fields_error")
    login(d, "locked_out_user")
    shot(d, "03_locked_out_user_error")
    login(d, "standard_user", "wrong")
    shot(d, "04_wrong_password_error")

    print("[2] Standard user happy path")
    login(d, "standard_user")
    shot(d, "05_inventory_standard_user")
    Select(d.find_element(By.CLASS_NAME, "product_sort_container")).select_by_value("lohi")
    time.sleep(0.5)
    prices = [float(p.text.strip("$")) for p in d.find_elements(By.CLASS_NAME, "inventory_item_price")]
    print("  standard_user price sort low->high:", prices, "sorted:", prices == sorted(prices))
    shot(d, "06_sort_price_low_high")
    d.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    d.find_element(By.ID, "add-to-cart-sauce-labs-bike-light").click()
    print("  cart badge:", d.find_element(By.CLASS_NAME, "shopping_cart_badge").text)
    shot(d, "07_items_added_badge")
    d.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    shot(d, "08_cart_page")
    d.find_element(By.ID, "checkout").click()
    d.find_element(By.ID, "continue").click()
    shot(d, "09_checkout_empty_form_error")
    d.find_element(By.ID, "first-name").send_keys("12345")
    d.find_element(By.ID, "last-name").send_keys("!!!")
    d.find_element(By.ID, "postal-code").send_keys("abc")
    d.find_element(By.ID, "continue").click()
    time.sleep(0.5)
    print("  checkout accepted numeric first name / letters in postal code:",
          "checkout-step-two" in d.current_url)
    shot(d, "10_checkout_invalid_data_accepted")
    total = d.find_element(By.CLASS_NAME, "summary_total_label").text
    sub = d.find_element(By.CLASS_NAME, "summary_subtotal_label").text
    tax = d.find_element(By.CLASS_NAME, "summary_tax_label").text
    print(" ", sub, "|", tax, "|", total)
    shot(d, "11_checkout_overview")
    d.find_element(By.ID, "finish").click()
    shot(d, "12_order_complete")
    d.find_element(By.ID, "react-burger-menu-btn").click()
    time.sleep(0.5)
    shot(d, "13_side_menu")
    d.find_element(By.ID, "logout_sidebar_link").click()
    time.sleep(0.5)
    print("  after logout url:", d.current_url)

    print("[3] Cart persists across logout (standard_user)")
    login(d, "standard_user")
    d.find_element(By.ID, "add-to-cart-sauce-labs-onesie").click()
    d.find_element(By.ID, "react-burger-menu-btn").click()
    time.sleep(0.5)
    d.find_element(By.ID, "logout_sidebar_link").click()
    login(d, "standard_user")
    badge = d.find_elements(By.CLASS_NAME, "shopping_cart_badge")
    print("  cart badge after re-login:", badge[0].text if badge else "none")
    shot(d, "14_cart_persists_after_relogin")
    if badge:
        d.find_element(By.ID, "remove-sauce-labs-onesie").click()

    print("[4] problem_user defects")
    login(d, "problem_user")
    srcs = {img.get_attribute("src") for img in d.find_elements(By.CLASS_NAME, "inventory_item_img")}
    print("  distinct product image sources:", len(srcs))
    shot(d, "15_problem_user_same_images")
    Select(d.find_element(By.CLASS_NAME, "product_sort_container")).select_by_value("lohi")
    time.sleep(0.5)
    prices = [float(p.text.strip("$")) for p in d.find_elements(By.CLASS_NAME, "inventory_item_price")]
    print("  problem_user price sort low->high:", prices, "sorted:", prices == sorted(prices))
    shot(d, "16_problem_user_sort_broken")
    d.find_element(By.ID, "add-to-cart-sauce-labs-fleece-jacket").click()
    d.find_element(By.ID, "add-to-cart-test.allthethings()-t-shirt-(red)").click()
    badge = d.find_elements(By.CLASS_NAME, "shopping_cart_badge")
    print("  problem_user badge after adding 2 items:", badge[0].text if badge else "none")
    shot(d, "17_problem_user_add_to_cart_fails")
    d.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    d.find_element(By.ID, "checkout").click()
    d.find_element(By.ID, "first-name").send_keys("Vishwajeet")
    d.find_element(By.ID, "last-name").send_keys("Tulse")
    d.find_element(By.ID, "postal-code").send_keys("411041")
    print("  problem_user last-name field value:", repr(d.find_element(By.ID, "last-name").get_attribute("value")))
    d.find_element(By.ID, "continue").click()
    time.sleep(0.5)
    shot(d, "18_problem_user_lastname_bug")

    print("[5] error_user and performance_glitch_user")
    login(d, "error_user")
    Select(d.find_element(By.CLASS_NAME, "product_sort_container")).select_by_value("za")
    time.sleep(0.8)
    try:
        alert = d.switch_to.alert
        print("  error_user sort alert:", alert.text)
        alert.accept()
    except Exception:
        print("  error_user: no alert")
    shot(d, "19_error_user_sort_alert")
    t0 = time.time()
    login(d, "performance_glitch_user")
    d.find_element(By.CLASS_NAME, "inventory_list")
    print(f"  performance_glitch_user login took {time.time() - t0:.1f} s")
    shot(d, "20_performance_glitch_user")

    print("[6] visual_user")
    login(d, "visual_user")
    shot(d, "21_visual_user_layout")

    print("[7] Remaining checks for the test-case sheet")
    d.get(URL)
    print("  password field type:", d.find_element(By.ID, "password").get_attribute("type"))
    print("  placeholders:", d.find_element(By.ID, "user-name").get_attribute("placeholder"),
          "/", d.find_element(By.ID, "password").get_attribute("placeholder"))
    d.delete_all_cookies()  # make sure nobody is logged in
    d.get(URL + "inventory.html")
    time.sleep(0.5)
    errs = d.find_elements(By.CSS_SELECTOR, "h3[data-test='error']")
    print("  direct /inventory.html when logged out:", errs[0].text if errs else "no error")
    shot(d, "22_direct_url_without_login")
    login(d, "standard_user")
    Select(d.find_element(By.CLASS_NAME, "product_sort_container")).select_by_value("za")
    time.sleep(0.5)
    names = [n.text for n in d.find_elements(By.CLASS_NAME, "inventory_item_name")]
    print("  name sort Z->A:", names == sorted(names, reverse=True), names[:2])
    d.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    d.find_element(By.ID, "add-to-cart-sauce-labs-bike-light").click()
    d.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    d.find_element(By.ID, "remove-sauce-labs-bike-light").click()
    print("  badge after removing one item on cart page:", d.find_element(By.CLASS_NAME, "shopping_cart_badge").text)
    shot(d, "23_remove_from_cart_page")
    d.find_element(By.ID, "continue-shopping").click()
    print("  continue shopping ->", d.current_url)
    d.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    d.find_element(By.ID, "checkout").click()
    d.find_element(By.ID, "first-name").send_keys("Vishwajeet")
    d.find_element(By.ID, "continue").click()
    print("  first name only ->", d.find_element(By.CSS_SELECTOR, "h3[data-test='error']").text)
    d.find_element(By.ID, "last-name").send_keys("Tulse")
    d.find_element(By.ID, "continue").click()
    print("  first+last name ->", d.find_element(By.CSS_SELECTOR, "h3[data-test='error']").text)
    d.find_element(By.ID, "cancel").click()
    print("  cancel ->", d.current_url)
    footer = d.find_element(By.CLASS_NAME, "footer_copy").text
    print("  footer:", footer[:40], "| social links:", len(d.find_elements(By.CSS_SELECTOR, "ul.social a")))
    d.find_element(By.ID, "react-burger-menu-btn").click()
    time.sleep(0.5)
    links = [a.text for a in d.find_elements(By.CSS_SELECTOR, ".bm-item-list a")]
    print("  menu links:", links)
    d.find_element(By.ID, "reset_sidebar_link").click()
    d.quit()
    print("Done.")


if __name__ == "__main__":
    main()
