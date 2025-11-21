# Product Specifications – E-Shop Checkout

## 1. Product Catalog
The checkout page supports the following products:

1. **Laptop**
   - Base Price: $999.99
   - Quantity limit: 1–10 per order

2. **Wireless Mouse**
   - Base Price: $29.99
   - Quantity limit: 1–10 per order

3. **USB-C Cable**
   - Base Price: $12.99
   - Quantity limit: 1–10 per order

All product price calculations must reflect:
`item_total = price × quantity`.

---

## 2. Discount Code Rules
The platform supports the following coupon rules:

| Code       | Discount % |
|------------|------------|
| SAVE10     | 10%        |
| SAVE15     | 15%        |
| SAVE20     | 20%        |
| WELCOME5   | 5%         |

Rules:
- Discount applies only to **subtotal before tax and shipping**.
- Only **one** discount code may be applied at a time.
- Discount value must be recalculated whenever the cart changes.

---

## 3. Tax Rules
- A **10% tax** is applied on `(subtotal - discount)`.

---

## 4. Shipping Rules
### Standard Shipping
- Cost: **$0.00**
- Delivery time: 5–7 business days

### Express Shipping
- Cost: **$10.00**
- Delivery time: 1–2 business days

Shipping cost is added **after** subtotal, discount, and tax.

---

## 5. Order Validation Rules
- Cart must contain **at least one product**.
- Full Name: minimum 3 characters.
- Street Address: minimum 10 characters.
- Email must follow standard email format.
- All fields are required.

---

## 6. Successful Payment
On valid input and cart contents:
- Display success message: **“Payment Successful!”**
- Hide form & product sections.
