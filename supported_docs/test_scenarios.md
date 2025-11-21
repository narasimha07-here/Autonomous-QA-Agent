# Test Scenarios – E-Shop Checkout System

This document outlines every major test scenario required to validate the complete functionality of the E-Shop Checkout page.  
Each scenario describes **what must be tested**, **why it must be tested**, and the **expected system behavior**.

---

## 1. Cart Management Scenarios

### TS-001: Add Valid Item to Cart
Validate that a user can add any product (Laptop, Mouse, USB-C Cable) with a valid quantity (1–10).

### TS-002: Reject Invalid Quantity
If quantity <1 or >10, system must display error alert and the product must not be added.

### TS-003: Update Cart Totals After Adding Product
Subtotal, tax, discount (if any), and final total must recalculate immediately based on new cart state.

### TS-004: Remove Item From Cart
When user removes an item, it should be deleted from cart display and totals must reflect the change.

### TS-005: Add Multiple Different Products
Cart should reflect multiple unique SKUs along with their individual quantities and totals.

---

## 2. Discount Code Scenarios

### TS-006: Apply Valid Discount Code
Valid codes: SAVE10, SAVE15, SAVE20, WELCOME5  
System must apply **correct percentage** and update totals.

### TS-007: Reject Invalid Discount Code
Invalid coupon should show red error message and discount must revert to 0.

### TS-008: Apply Discount After Cart Update  
Discount must remain active if cart changes — totals must recalculate correctly.

### TS-009: Apply Discount After Shipping Method Change  
Changing shipping (Standard ↔ Express) must not reset the coupon.

### TS-010: Empty Input Discount Code
If user clicks “Apply” with empty field, red error message should appear.

---

## 3. Shipping Method Scenarios

### TS-011: Default Shipping Option
Standard shipping should be selected by default and cost shown as $0.00.

### TS-012: Select Express Shipping
Choosing Express must add $10 to total.

### TS-013: Change Shipping After Cart Changes
Totals must recalculate properly even if cart changes after selecting shipping.

---

## 4. Billing & User Information Scenarios

### TS-014: Validate Required Fields
Full Name, Email, Address, City, State, ZIP, Country are all required.

### TS-015: Full Name Validation
Input less than 3 characters must trigger error.

### TS-016: Email Format Validation
Invalid email format must show red error and prevent submission.

### TS-017: Address Validation
Address fewer than 10 characters should trigger error.

### TS-018: ZIP Code Validations
ZIP must not be empty and should reflect error state on invalid input.

### TS-019: Country Field Required Check  
Country must not be blank—error should appear if missing.

---

## 5. Payment Method Scenarios

### TS-020: Default Payment Method
Credit Card must be selected by default.

### TS-021: Change Payment Method
Switching to PayPal must work correctly.

---

## 6. End-to-End Checkout Scenarios

### TS-022: Successful Checkout With Valid Input
User fills all fields correctly + cart has items → payment shows **“Payment Successful!”**

### TS-023: Block Checkout on Invalid Form
If any field is invalid, checkout must be blocked and success message must not appear.

### TS-024: Block Checkout When Cart is Empty  
If user submits form with empty cart → alert “Cart is empty”.

### TS-025: Successful Checkout With Discount Applied  
Correct discount must persist through entire checkout flow.

### TS-026: Successful Checkout With Express Shipping  
Final total should include express fee and success message shown.

---

## 7. UI / UX Scenarios

### TS-027: Error Messages Display in Red  
All validation errors must follow UI-UX guideline (red text + red bar + light red background).

### TS-028: Success Box Display After Payment  
Green success box must appear and hide:
- product section  
- discount section  
- checkout form  

### TS-029: Pay Now Button Styling  
Button must be green and show hover darkening effect.

### TS-030: Responsive Layout  
Fields must stack vertically on screens < 768px.

---

## 8. Boundary & Negative Scenarios

### TS-031: Quantity Boundary Values  
Test qty=1 (min) and qty=10 (max).

### TS-032: Extreme Invalid Quantity  
Negative qty, 0, >10 must be rejected.

### TS-033: Empty Form Submission  
Press Pay Now without entering any values → required field errors must appear.

### TS-034: Apply Multiple Discount Attempts  
Only one valid coupon must be applied at a time.

### TS-035: Refresh After Payment  
After refresh, cart and discount status must reset to initial state.

---

## 9. System Behavior Scenarios

### TS-036: Correct Tax Calculation  
Tax must always be 10% of (subtotal − discount).

### TS-037: Totals Should Update Reactively  
Any change in cart, discount, or shipping must update totals instantly.

### TS-038: JavaScript Error-Free Execution  
Page console must show no JS errors during normal flows.

---

# End of Test Scenarios
