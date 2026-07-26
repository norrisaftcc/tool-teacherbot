# M1LAB: The Campus Coffee Shop Point of Sale System

## The Scenario
The campus coffee shop "Byte Brew Café" just lost their point-of-sale system to a power surge. The owner needs a temporary solution for tomorrow's morning rush. You've volunteered to create a simple C++ program that can calculate a typical morning order, apply discounts, compute tax, and generate a receipt. The owner will hardcode tomorrow's special order details into the program tonight.

This is a real emergency - the shop opens at 7 AM and serves over 200 students before first period!

## Learning Objectives
By completing this lab, you will:
- Perform arithmetic operations with multiple data types
- Handle currency calculations with proper precision
- Apply business logic through mathematical operations
- Format output to create professional receipts
- Debug calculation errors systematically

## Background: The Business Rules
Byte Brew Café has specific pricing rules:
- All prices include cents (use `double` type)
- Student discount: 15% off the subtotal
- Sales tax: 7.5% applied AFTER discount
- Loyalty points: 1 point per dollar spent (after tax)
- Morning rush special: Buy 3 or more drinks, get 10% off drinks only

## Part 1: Understanding the Requirements (20 points)

### The Order to Calculate
Tomorrow morning, the Computer Science club is placing their regular Wednesday order:
- 4 Large Coffees @ $3.50 each
- 3 Breakfast Sandwiches @ $6.75 each  
- 2 Muffins @ $2.25 each
- 5 Energy Drinks @ $4.00 each

They have a student discount and pay with a $100 bill.

### Your Planning Phase
Before coding, calculate by hand:
1. Subtotal for each category
2. Apply morning special to drinks
3. Apply student discount
4. Add tax
5. Calculate change from $100

**Deliverable:** Include your hand calculations as comments in your code for verification.

## Part 2: Building the POS System (50 points)

### Step 2.1: Create Your Program File
Create: `m1lab_lastname.cpp`

### Step 2.2: Program Structure
```cpp
/*
    CSC 134
    M1LAB - Coffee Shop POS System
    [Your Name]
    [Date]
    
    Emergency POS system for Byte Brew Café
    Calculates order total with discounts and tax
    
    Hand Calculations for Verification:
    Coffee subtotal: 4 × $3.50 = $14.00
    [Continue your calculations here...]
*/

#include <iostream>
#include <iomanip>  // For currency formatting
#include <string>
using namespace std;

int main() {
    // Store information
    string shopName = "Byte Brew Café";
    string orderNumber = "ORDER #2024-001";
    
    // Prices (in dollars)
    double coffeePrice = 3.50;
    double sandwichPrice = 6.75;
    double muffinPrice = 2.25;
    double energyDrinkPrice = 4.00;
    
    // Quantities
    int coffeeQty = 4;
    int sandwichQty = 3;
    int muffinQty = 2;
    int energyDrinkQty = 5;
    
    // Business rules
    double studentDiscountRate = 0.15;  // 15%
    double morningSpecialRate = 0.10;   // 10% off drinks
    double salesTaxRate = 0.075;        // 7.5%
    double paymentAmount = 100.00;
    
    // Your calculations will go here
    
    return 0;
}
```

### Step 2.3: Required Calculations

Implement these calculations in order:

1. **Calculate line item subtotals:**
```cpp
double coffeeSubtotal = coffeePrice * coffeeQty;
double sandwichSubtotal = sandwichPrice * sandwichQty;
// Continue for all items...
```

2. **Calculate drink totals for morning special:**
```cpp
double totalDrinks = coffeeSubtotal + energyDrinkSubtotal;
int totalDrinkQty = coffeeQty + energyDrinkQty;
double drinkDiscount = 0.0;

if (totalDrinkQty >= 3) {
    drinkDiscount = totalDrinks * morningSpecialRate;
}
```

3. **Calculate subtotal after morning special:**
```cpp
double subtotalAfterSpecial = /* your calculation */;
```

4. **Apply student discount:**
```cpp
double studentDiscount = subtotalAfterSpecial * studentDiscountRate;
double subtotalAfterDiscounts = subtotalAfterSpecial - studentDiscount;
```

5. **Calculate tax and final total:**
```cpp
double taxAmount = subtotalAfterDiscounts * salesTaxRate;
double finalTotal = subtotalAfterDiscounts + taxAmount;
```

6. **Calculate change and loyalty points:**
```cpp
double changeAmount = paymentAmount - finalTotal;
int loyaltyPoints = (int)finalTotal;  // 1 point per dollar
```

### Step 2.4: Format the Receipt

Create a professional receipt output:

```cpp
// Set decimal precision for currency
cout << fixed << setprecision(2);

cout << "\n========================================" << endl;
cout << "           " << shopName << "           " << endl;
cout << "        " << orderNumber << "        " << endl;
cout << "========================================" << endl;
cout << "\nITEMIZED ORDER:" << endl;
cout << "----------------------------------------" << endl;

// Item listings with alignment
cout << left << setw(25) << "Large Coffee" 
     << "x" << coffeeQty 
     << right << setw(10) << "$" << coffeeSubtotal << endl;
// Continue for all items...

cout << "----------------------------------------" << endl;
cout << left << setw(30) << "Subtotal:" 
     << right << setw(10) << "$" << /* subtotal */ << endl;

// Show discounts applied
if (drinkDiscount > 0) {
    cout << left << setw(30) << "Morning Special (drinks):" 
         << right << setw(10) << "-$" << drinkDiscount << endl;
}

// Continue with all discounts, tax, total...

cout << "========================================" << endl;
cout << left << setw(30) << "TOTAL:" 
     << right << setw(10) << "$" << finalTotal << endl;
cout << left << setw(30) << "PAID:" 
     << right << setw(10) << "$" << paymentAmount << endl;
cout << left << setw(30) << "CHANGE:" 
     << right << setw(10) << "$" << changeAmount << endl;
cout << "========================================" << endl;
cout << "\nLoyalty Points Earned: " << loyaltyPoints << endl;
cout << "\n   Thank you for choosing Byte Brew!   " << endl;
cout << "          Have a great day!            " << endl;
cout << "========================================\n" << endl;
```

## Part 3: Testing and Validation (20 points)

### Step 3.1: Verify Calculations
Your final total should be approximately $47.87 (you'll calculate the exact amount).
If your numbers don't match:
1. Check order of operations
2. Verify discount applications
3. Ensure tax is calculated on the discounted amount

### Step 3.2: Edge Case Testing
Modify your quantities to test:
1. What happens with 2 drinks? (morning special shouldn't apply)
2. What if payment is exactly the total?
3. What if there are 0 of an item?

Document your test results in comments.

## Part 4: Professional Enhancement (10 points)

Add ONE of the following features:

### Option A: Daily Summary
Calculate and display:
- Total revenue for the day (assuming 50 similar orders)
- Total tax collected
- Total discounts given

### Option B: Inventory Alert
Track inventory and warn if running low:
```cpp
int coffeeInventory = 100;  // cups available
coffeeInventory -= coffeeQty;
if (coffeeInventory < 20) {
    cout << "⚠ WARNING: Low coffee inventory!" << endl;
}
```

### Option C: Tip Suggestion
Calculate and display suggested tip amounts:
```cpp
cout << "\nSUGGESTED TIPS:" << endl;
cout << "  15%: $" << finalTotal * 0.15 << endl;
cout << "  18%: $" << finalTotal * 0.18 << endl;
cout << "  20%: $" << finalTotal * 0.20 << endl;
```

## Submission Requirements

1. **Source code:** `m1lab_lastname.cpp`
2. **Screenshot:** Complete receipt output
3. **GitHub link:** To your committed file

## Grading Rubric (100 points)

### Planning and Analysis (20 points)
- **Excellent (18-20):** Hand calculations shown and correct
- **Good (15-17):** Calculations present with minor errors
- **Satisfactory (12-14):** Basic planning shown
- **Needs Improvement (0-11):** Minimal planning

### Calculation Implementation (30 points)
- **Excellent (28-30):** All calculations correct, efficient code
- **Good (24-27):** Most calculations correct, good code
- **Satisfactory (20-23):** Basic calculations work
- **Needs Improvement (0-19):** Major calculation errors

### Receipt Formatting (20 points)
- **Excellent (18-20):** Professional, aligned, complete receipt
- **Good (15-17):** Good formatting, minor issues
- **Satisfactory (12-14):** Readable receipt, some formatting issues
- **Needs Improvement (0-11):** Poor formatting

### Testing and Validation (20 points)
- **Excellent (18-20):** Thorough testing documented, edge cases considered
- **Good (15-17):** Good testing, most cases covered
- **Satisfactory (12-14):** Basic testing performed
- **Needs Improvement (0-11):** Minimal testing

### Enhancement Feature (10 points)
- **Excellent (9-10):** Feature works perfectly, adds value
- **Good (7-8):** Feature works with minor issues
- **Satisfactory (5-6):** Basic feature attempted
- **Needs Improvement (0-4):** Feature missing or broken

## Common Pitfalls and Solutions

### Floating Point Precision Issues
**Problem:** $19.99 displays as $19.990000  
**Solution:** Use `fixed` and `setprecision(2)`

### Incorrect Discount Order
**Problem:** Tax calculated before discount  
**Solution:** Always: subtotal → discounts → tax → total

### Integer Division Errors
**Problem:** 5/2 equals 2 instead of 2.5  
**Solution:** Ensure at least one operand is a double: `5.0/2`

### Alignment Issues
**Problem:** Receipt columns don't line up  
**Solution:** Use `setw()` and `left`/`right` manipulators

## Real-World Connection
This assignment simulates actual POS systems used in businesses. The skills you're practicing:
- **Precision in financial calculations** - Errors cost real money
- **User-friendly output** - Customers need clear receipts
- **Business logic implementation** - Discounts and tax rules
- **Testing and validation** - Ensuring accuracy before deployment

Professional developers build similar systems for:
- Retail stores
- Restaurants  
- Online shopping carts
- Banking applications

## Extension Challenges (Optional)

### Challenge 1: Multi-Currency Support (+5 points)
Add support for payment in euros (1 EUR = 1.10 USD)

### Challenge 2: Happy Hour Pricing (+5 points)
Implement time-based pricing (imagine it's 3 PM and happy hour started)

### Challenge 3: Combo Meal Detection (+5 points)
Automatically detect and apply combo pricing when certain items are ordered together

## Tips for Success
1. **Test frequently** - Compile and run after each calculation section
2. **Use meaningful variable names** - `coffeeSubtotal` not `cs`
3. **Comment your calculations** - Explain complex formulas
4. **Check your math** - Use a calculator to verify
5. **Format incrementally** - Get calculations working before beautifying output

## Next Assignment Preview
In M1HW1, you'll expand this system to accept user input, allowing real-time order entry. You'll also add features like multiple payment methods and customer loyalty lookups.

## Reflection Prompt
After completing this lab, consider:
- How do data types affect calculation accuracy?
- Why is the order of operations important in business calculations?
- What would happen if this system had a calculation error in a real shop?

Remember: In the real world, financial calculation errors can lead to lost revenue, customer dissatisfaction, and legal issues. Take pride in getting it right!