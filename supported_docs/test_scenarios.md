# Test Scenarios for E-Commerce Checkout System

## Cart Management Tests

### Positive Test Cases
- **TC_CART_001**: Add single product to cart and verify item appears
- **TC_CART_002**: Add multiple different products to cart
- **TC_CART_003**: Increase quantity of product in cart
- **TC_CART_004**: Decrease quantity of product in cart
- **TC_CART_005**: Remove product from cart
- **TC_CART_006**: Verify cart total is calculated correctly
- **TC_CART_007**: Clear entire cart

### Negative Test Cases
- **TC_CART_008**: Add quantity exceeding maximum (10 units)
- **TC_CART_009**: Add quantity as 0
- **TC_CART_010**: Add negative quantity
- **TC_CART_011**: Try to checkout with empty cart

## Discount Code Tests

### Positive Test Cases
- **TC_DISC_001**: Apply valid discount code SAVE10
- **TC_DISC_002**: Apply valid discount code SAVE15
- **TC_DISC_003**: Apply valid discount code SAVE20
- **TC_DISC_004**: Apply valid discount code WELCOME5
- **TC_DISC_005**: Verify discount percentage applied correctly
- **TC_DISC_006**: Verify discount amount calculated correctly
- **TC_DISC_007**: Verify tax calculated on discounted amount

### Negative Test Cases
- **TC_DISC_008**: Apply invalid discount code
- **TC_DISC_009**: Apply discount code with special characters
- **TC_DISC_010**: Apply discount code with lowercase (case-insensitivity)
- **TC_DISC_011**: Apply multiple discount codes (should reject second one)
- **TC_DISC_012**: Apply expired discount code
- **TC_DISC_013**: Apply discount code to empty cart

## Shipping Tests

### Positive Test Cases
- **TC_SHIP_001**: Select Standard Shipping (Free)
- **TC_SHIP_002**: Select Express Shipping ($10)
- **TC_SHIP_003**: Verify Standard shipping adds $0 to total
- **TC_SHIP_004**: Verify Express shipping adds $10 to total
- **TC_SHIP_005**: Change shipping method and verify total updates

### Negative Test Cases
- **TC_SHIP_006**: Proceed to checkout without selecting shipping method
- **TC_SHIP_007**: Select invalid shipping method

## User Information Validation Tests

### Full Name Validation
- **TC_NAME_001**: Enter valid full name (3+ characters)
- **TC_NAME_002**: Enter name with 2 characters (invalid)
- **TC_NAME_003**: Enter empty name field
- **TC_NAME_004**: Enter name with special characters
- **TC_NAME_005**: Enter name exceeding 50 characters

### Email Validation
- **TC_EMAIL_001**: Enter valid email format (user@example.com)
- **TC_EMAIL_002**: Enter email without @ symbol
- **TC_EMAIL_003**: Enter email without domain
- **TC_EMAIL_004**: Enter empty email field
- **TC_EMAIL_005**: Enter email with spaces
- **TC_EMAIL_006**: Verify error message displays for invalid email

### Address Validation
- **TC_ADDR_001**: Enter valid street address (10+ characters)
- **TC_ADDR_002**: Enter street address with less than 10 characters
- **TC_ADDR_003**: Enter valid city name
- **TC_ADDR_004**: Enter empty city field
- **TC_ADDR_005**: Enter valid state/province
- **TC_ADDR_006**: Enter valid zip/postal code
- **TC_ADDR_007**: Enter valid country
- **TC_ADDR_008**: Verify all address fields are required

## Payment Method Tests

### Positive Test Cases
- **TC_PAY_001**: Select Credit Card payment method
- **TC_PAY_002**: Select PayPal payment method
- **TC_PAY_003**: Verify selected payment method is highlighted

### Negative Test Cases
- **TC_PAY_004**: Proceed to checkout without selecting payment method

## Order Submission Tests

### Successful Submission
- **TC_ORDER_001**: Submit complete order with all valid information
- **TC_ORDER_002**: Verify "Payment Successful!" message displays
- **TC_ORDER_003**: Verify order ID is generated
- **TC_ORDER_004**: Verify cart is cleared after successful order

### Failed Submission
- **TC_ORDER_005**: Submit order with missing required field (name)
- **TC_ORDER_006**: Submit order with missing required field (email)
- **TC_ORDER_007**: Submit order with missing required field (address)
- **TC_ORDER_008**: Submit order with invalid email format
- **TC_ORDER_009**: Submit order with empty cart
- **TC_ORDER_010**: Verify appropriate error messages display for each validation failure

## Price Calculation Tests

### Tax Calculation
- **TC_TAX_001**: Verify tax calculated at 10% on subtotal
- **TC_TAX_002**: Verify tax calculated on amount AFTER discount applied
- **TC_TAX_003**: Verify tax rounded to 2 decimal places
- **TC_TAX_004**: Verify final total = (Subtotal - Discount) + Tax + Shipping

### Total Amount Verification
- **TC_TOTAL_001**: Verify total with no discount, standard shipping
- **TC_TOTAL_002**: Verify total with discount, standard shipping
- **TC_TOTAL_003**: Verify total with no discount, express shipping
- **TC_TOTAL_004**: Verify total with discount and express shipping

## UI/UX Tests

### Error Message Display
- **TC_UI_001**: Verify error messages display in red color
- **TC_UI_002**: Verify error messages appear below respective input fields
- **TC_UI_003**: Verify error messages have proper formatting

### Button Styling
- **TC_UI_004**: Verify "Pay Now" button is green
- **TC_UI_005**: Verify "Add to Cart" buttons are blue
- **TC_UI_006**: Verify buttons have proper hover states
- **TC_UI_007**: Verify disabled buttons show cursor not-allowed

### Form Validation Indicators
- **TC_UI_008**: Verify red asterisk (*) displays next to required fields
- **TC_UI_009**: Verify checkmark displays for valid input
- **TC_UI_010**: Verify X mark displays for invalid input

## Edge Cases

### Boundary Tests
- **TC_EDGE_001**: Order with minimum value ($0.01)
- **TC_EDGE_002**: Order with very large value ($99,999.99)
- **TC_EDGE_003**: Add maximum quantity (10) of each product
- **TC_EDGE_004**: Apply discount that reduces total to near $0.01

### Session Tests
- **TC_SESSION_001**: Verify cart persists during single session
- **TC_SESSION_002**: Verify cart clears after successful order
- **TC_SESSION_003**: Verify form data persists during session

## Accessibility Tests

### Keyboard Navigation
- **TC_ACC_001**: Navigate form using Tab key
- **TC_ACC_002**: Submit form using Enter key
- **TC_ACC_003**: Verify all interactive elements are keyboard accessible

### Screen Reader Compatibility
- **TC_ACC_004**: Verify all form labels are properly associated
- **TC_ACC_005**: Verify error messages are announced to screen readers
- **TC_ACC_006**: Verify success messages are announced to screen readers
