# Manual Testing of an E-Commerce Website Using Test Cases and Bug Reports

Mini project for **Software Testing and Quality Assurance (Manual Testing)**,
Laboratory Practice IV, BE Computer Engineering, Savitribai Phule Pune University.

**Application under test:** Swag Labs demo store, https://www.saucedemo.com
(a public e-commerce demo with login, product catalogue, cart and checkout, and
several test users that expose deliberate defects).

## What was done

1. Wrote a **test plan** and **20 test scenarios** covering login, products, cart, checkout, menu and UI.
2. Wrote **39 test cases** in an Excel sheet with pre-conditions, steps, test data, expected and actual results.
3. Executed every test case manually in Microsoft Edge with six different test users.
4. Logged **9 defects** with severity, priority, steps to reproduce and screenshot evidence.
5. Prepared a **requirement traceability matrix (RTM)** and a summary sheet.

Result: 28 passed, 11 failed, 9 defects (1 critical, 3 high, 5 medium).

## Repository layout

```
docs/Test_Plan.md              scope, strategy, environment, schedule
docs/Test_Scenarios.md         20 scenarios mapped to test cases
docs/Test_Cases.md             the test cases as a Markdown table
docs/Defect_Reports.md         9 defect reports with screenshots
test_cases/SwagLabs_Test_Cases.xlsx
                               sheets: Test Cases, Defect Reports, RTM, Summary
screenshots/                   evidence captured during execution
tools/capture_evidence.py      re-creates the evidence screenshots (Selenium)
tools/build_documents.py       builds the Excel workbook and Markdown docs
report/                        LaTeX project report (SPPU BE format)
```

## Defects found (summary)

| ID | Summary | Severity |
|---|---|---|
| DEF-01 | Wrong product images for problem_user | High |
| DEF-02 | Price sorting does not reorder products for problem_user | Medium |
| DEF-03 | Add to cart has no effect for some products (problem_user) | High |
| DEF-04 | Last Name field cannot be filled during checkout (problem_user) | Critical |
| DEF-05 | Checkout form accepts invalid data (all users) | Medium |
| DEF-06 | Cart contents persist after logout and re-login | Medium |
| DEF-07 | Sorting shows a JavaScript alert for error_user | Medium |
| DEF-08 | Login takes about 7 seconds for performance_glitch_user | Medium |
| DEF-09 | Wrong prices and misaligned layout for visual_user | High |

## Re-generating the documents

```bash
pip install openpyxl selenium
python tools/capture_evidence.py     # screenshots (needs Edge or Chrome)
python tools/build_documents.py      # Excel workbook + Markdown docs
```
