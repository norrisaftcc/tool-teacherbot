# M2T1: The Interactive Farmer's Market Stand

## The Scenario
Remember the apple orchard from Module 1? Jane Smith was so impressed with your point-of-sale system that she's recommended you to the entire Farmer's Market Association! Now they want you to create an interactive version that any vendor can use. Instead of hardcoding "apples" and "Jane Smith," the program will ask vendors to input their own information each morning when they set up their stand.

This is your first interactive program - one that responds to whoever is using it!

## Learning Objectives
By completing this assignment, you will:
- Use `cin` to get user input for different data types
- Create prompts that clearly tell users what to enter
- Build a dynamic program that works for any vendor
- Handle the transition from hardcoded to user-provided values
- Debug common input issues

## Background: From Static to Interactive
In M1LAB, you wrote:
```cpp
string name = "Jane Smith";
int apples = 100;
double pricePerApple = 0.25;
```

Now you'll transform this into:
```cpp
string name;
cout << "Enter your name: ";
cin >> name;
// Continue for other variables...
```

The program becomes a conversation between the computer and the user!

## Part 1: Planning the Interaction (15 points)

### User Experience Design
Before coding, plan the conversation flow:
1. Welcome message
2. What information to collect (in what order)
3. How to phrase each prompt clearly
4. What to display back to confirm

**Deliverable:** Include your conversation flow as comments in your code

## Part 2: Building the Interactive Market Stand (60 points)

### Step 2.1: Create Your Program File
Create: `m2t1_lastname.cpp`

### Step 2.2: Professional Header
```cpp
/*
    CSC 134
    M2T1 - Interactive Farmer's Market
    [Your Name]
    [Date]
    
    This program creates an interactive point-of-sale system
    that any farmer's market vendor can customize with their
    own products and prices.
    
    Conversation Flow:
    1. Greet vendor and get their name
    2. Ask what product they're selling
    3. Get quantity and price information
    4. Calculate and display results
*/
```

### Step 2.3: Implement the Interactive System

```cpp
#include <iostream>
#include <iomanip>
#include <string>
using namespace std;

int main() {
    // Display welcome banner
    cout << "=====================================" << endl;
    cout << "  FARMER'S MARKET SETUP WIZARD      " << endl;
    cout << "=====================================" << endl;
    cout << endl;
    
    // Vendor information
    string vendorName;
    string standName;
    
    cout << "Good morning! Let's set up your stand for today." << endl;
    cout << "What is your name? ";
    cin >> vendorName;
    
    cout << "What would you like to call your stand? ";
    cin.ignore(); // Clear the input buffer
    getline(cin, standName);
    
    // Product information
    string productName;
    int quantity;
    double pricePerUnit;
    
    cout << "\nNow let's set up your inventory." << endl;
    cout << "What product are you selling today? ";
    getline(cin, productName);
    
    cout << "How many " << productName << " do you have? ";
    cin >> quantity;
    
    cout << "What is the price per " << productName << "? $";
    cin >> pricePerUnit;
    
    // Calculations
    double totalValue = quantity * pricePerUnit;
    
    // Special offers
    cout << "\nWould you like to offer a bulk discount?" << endl;
    cout << "Enter discount percentage (0 for none): ";
    double discountPercent;
    cin >> discountPercent;
    
    double bulkPrice = totalValue * (1 - discountPercent/100);
    
    // Display the customized stand information
    cout << "\n=====================================" << endl;
    cout << "     " << standName << "     " << endl;
    cout << "     Operated by " << vendorName << endl;
    cout << "=====================================" << endl;
    cout << fixed << setprecision(2);
    cout << "\nToday's Special: " << productName << endl;
    cout << "Quantity Available: " << quantity << endl;
    cout << "Price per unit: $" << pricePerUnit << endl;
    cout << "-------------------------------------" << endl;
    cout << "Total inventory value: $" << totalValue << endl;
    
    if (discountPercent > 0) {
        cout << "\n*** BULK SPECIAL ***" << endl;
        cout << "Buy all " << quantity << " for just $" << bulkPrice << endl;
        cout << "Save " << discountPercent << "%!" << endl;
    }
    
    cout << "\nYour stand is ready for customers!" << endl;
    cout << "Have a successful day at the market!" << endl;
    
    return 0;
}
```

### Step 2.4: Testing Your Program

Test with different inputs:
1. **Single-word inputs:** Name = "Jane", Product = "Apples"
2. **Multi-word inputs:** Stand name = "Smith Family Farm"
3. **Various numbers:** Price = 0.50, Quantity = 200
4. **Edge cases:** Discount = 0, Very large quantities

## Part 3: Handling Input Challenges (25 points)

### Common Issue #1: The Name Problem
When you run the program, you might notice if you enter "Jane Smith" for the name, only "Jane" is stored. This is because `cin >>` stops at spaces.

**Document this behavior** in your code comments and explain why it happens.

### Common Issue #2: The Buffer Problem
After using `cin >>`, there's often a newline character left in the input buffer. This can cause `getline()` to read an empty line.

**Solution demonstrated:** 
```cpp
cin >> number;
cin.ignore(); // Clear the leftover newline
getline(cin, text);
```

### Enhancement: Improve Name Handling
For bonus points (+5), modify the vendor name input to accept full names:
```cpp
cout << "What is your name? ";
cin.ignore(); // Clear any existing buffer
getline(cin, vendorName);
```

## Submission Requirements

1. **Source code:** `m2t1_lastname.cpp`
2. **Screenshot:** Three test runs with different products
3. **Reflection:** One paragraph about input challenges you encountered

## Grading Rubric (100 points)

### Planning and Design (15 points)
- **Excellent (14-15):** Clear conversation flow documented
- **Good (12-13):** Good planning evident
- **Satisfactory (10-11):** Basic planning present
- **Needs Improvement (0-9):** Minimal planning

### Core Functionality (35 points)
- **Excellent (33-35):** All inputs work correctly, smooth interaction
- **Good (28-32):** Most inputs work, minor issues
- **Satisfactory (23-27):** Basic input functionality
- **Needs Improvement (0-22):** Major input problems

### Calculations and Output (25 points)
- **Excellent (23-25):** Correct calculations, professional output
- **Good (20-22):** Mostly correct with good formatting
- **Satisfactory (17-19):** Basic calculations work
- **Needs Improvement (0-16):** Calculation errors

### Input Challenge Handling (25 points)
- **Excellent (23-25):** Both issues addressed and documented
- **Good (20-22):** Issues recognized and partially addressed
- **Satisfactory (17-19):** Basic awareness of issues
- **Needs Improvement (0-16):** Issues not addressed

## Sample Interaction
```
=====================================
  FARMER'S MARKET SETUP WIZARD      
=====================================

Good morning! Let's set up your stand for today.
What is your name? Maria
What would you like to call your stand? Maria's Fresh Produce

Now let's set up your inventory.
What product are you selling today? Organic Tomatoes
How many Organic Tomatoes do you have? 50
What is the price per Organic Tomatoes? $2.50

Would you like to offer a bulk discount?
Enter discount percentage (0 for none): 15

=====================================
     Maria's Fresh Produce     
     Operated by Maria
=====================================

Today's Special: Organic Tomatoes
Quantity Available: 50
Price per unit: $2.50
-------------------------------------
Total inventory value: $125.00

*** BULK SPECIAL ***
Buy all 50 for just $106.25
Save 15%!

Your stand is ready for customers!
Have a successful day at the market!
```

## Common Mistakes to Avoid
- **No prompts:** Always tell the user what to enter
- **Buffer issues:** Remember `cin.ignore()` when mixing input methods
- **No input validation:** For now, assume valid input (we'll add validation in Module 3)
- **Poor formatting:** Use `setprecision` for currency

## Extension Challenges (Optional Bonus)

### Challenge 1: Multiple Products (+5 points)
Allow the vendor to set up 3 different products

### Challenge 2: Daily Goals (+5 points)
Ask for a sales goal and calculate how many units need to be sold

### Challenge 3: Time-based Pricing (+5 points)
Add "morning price" and "afternoon price" options

## Why This Matters
Interactive programs are the foundation of user-facing software. Every app, website, and system you use started with someone figuring out how to get input from users and respond appropriately. This assignment teaches you to think about the user experience, handle input gracefully, and create programs that work for anyone, not just one hardcoded scenario.

## Reflection Questions
1. What's the difference between `cin >>` and `getline()`?
2. Why do we need to prompt users before asking for input?
3. How does making a program interactive change how you test it?

## Next Steps
In M2T2, you'll create a restaurant bill calculator that handles multiple calculations based on user input, introducing percentage calculations and more complex formatting.