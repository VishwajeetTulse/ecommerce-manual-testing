# Test Plan - Manual Testing of Swag Labs (E-Commerce Website)

| Item | Detail |
|---|---|
| Application under test | Swag Labs demo store, https://www.saucedemo.com |
| Document version | 1.0 |
| Prepared by | Vishwajeet Tulse and group (BE Computer, NBN SSOE) |
| Course | Laboratory Practice IV, Software Testing and Quality Assurance |

## 1. Introduction

Swag Labs is a public demo e-commerce website that provides login, a product
catalogue, a shopping cart and a checkout flow. It ships with several test
user accounts, some of which deliberately expose defects. This plan describes
how the site is tested manually to find and document those defects.

## 2. Objectives

1. Verify that the main user journey (login, browse, add to cart, checkout, logout) works.
2. Verify input validation on the login and checkout forms with positive and negative data.
3. Find, reproduce and document defects with severity, priority and evidence.
4. Produce a test-case sheet, defect reports and a requirement traceability matrix.

## 3. Scope

**In scope**

- Login module (valid, invalid, empty, locked-out and slow users)
- Products page (listing, sorting, images, prices)
- Cart (add, remove, badge count, persistence)
- Checkout (information form validation, overview totals, order completion)
- Side menu and navigation (logout, protected pages)
- Basic UI checks (placeholders, button states, footer)

**Out of scope**

- Payment gateway (the demo uses a fixed dummy card)
- Load / stress testing, security penetration testing
- Mobile devices and browsers other than Microsoft Edge

## 4. Test strategy

| Type | How it is applied |
|---|---|
| Functional testing | Each feature is tested against its expected behaviour |
| Negative testing | Invalid, empty and boundary inputs on every form |
| UI testing | Elements present, aligned and labelled correctly |
| Regression | Full sheet re-executed after each site change |
| Technique | Black-box: equivalence partitioning and boundary values for form fields; error guessing using the special test users |

## 5. Test users

| Username | Purpose |
|---|---|
| standard_user | normal user, baseline behaviour |
| locked_out_user | login must be refused |
| problem_user | user with visible functional bugs |
| performance_glitch_user | slow responses |
| error_user | user that triggers errors |
| visual_user | user with visual / layout bugs |

Password for all users: `secret_sauce`.

## 6. Test environment

- Windows 11 Home, Microsoft Edge 142
- Screen 1280 x 900
- Internet connection to https://www.saucedemo.com

## 7. Entry and exit criteria

**Entry:** site reachable, test users known, test cases reviewed by the guide.

**Exit:** all planned test cases executed, every failure linked to a defect report with a screenshot, summary sheet prepared.

## 8. Deliverables

- `test_cases/SwagLabs_Test_Cases.xlsx` (Test Cases, Defect Reports, RTM, Summary sheets)
- `docs/Test_Scenarios.md`, `docs/Test_Cases.md`, `docs/Defect_Reports.md`
- `screenshots/` evidence
- Project report (`report/report.pdf`)

## 9. Severity and priority scale

| Severity | Meaning |
|---|---|
| Critical | Blocks a main flow (e.g. cannot complete checkout) |
| High | Major feature wrong (wrong price, wrong product image, cannot add to cart) |
| Medium | Feature works partly or with workaround (sorting, validation) |
| Low | Cosmetic |

Priority (High / Medium / Low) states how soon the developer should fix it.

## 10. Schedule

| Week | Activity |
|---|---|
| 1 | Study the site, write test scenarios and SRS summary |
| 2 | Write test cases in Excel, review with guide |
| 3 | Execute test cases, capture evidence, log defects |
| 4 | Summary, RTM, project report |

## 11. Risks

- The public demo site may change (e.g. a new menu link appeared during testing); test cases are re-checked before final execution.
- Internet outage during execution; mitigated by keeping screenshots locally.
