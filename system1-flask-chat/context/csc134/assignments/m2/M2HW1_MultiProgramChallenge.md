# M2HW1: Multi-Program Challenge - Real-World Applications

## Overview
This homework combines multiple real-world programming challenges, introducing our **Tiered Grading System**. You choose your target grade by selecting how many programs to complete. Each program solves a different practical problem, reinforcing the input, calculation, and output skills from Module 2.

## Tiered Grading System

### Choose Your Challenge Level:
- **🥉 Bronze (up to 80%):** Complete any 2 programs
- **🥈 Silver (up to 90%):** Complete any 3 programs  
- **🥇 Gold (up to 100%):** Complete all 4 programs
- **💎 Diamond (up to 110%):** All 4 programs + all suggested improvements

**IMPORTANT:** Declare your tier in your header comment:
```cpp
/*
    CSC 134
    M2HW1 - Gold Tier
    [Your Name]
    [Date]
*/
```

## Program Structure Options
You can either:
1. **Single file:** Create one program with all questions (use menu or sequential execution)
2. **Multiple files:** Create separate programs (m2hw1_q1_lastname.cpp, etc.)

Always label output clearly: "Question 1: Banking System" etc.

---

## Question 1: Personal Banking System

### The Scenario
Create a banking transaction simulator for FTCC Federal Credit Union's new mobile app prototype.

### Requirements
The program should:
1. Ask for the account holder's name
2. Request:
   - Starting account balance
   - Deposit amount
   - Withdrawal amount
3. Generate a unique account number (you choose the method)
4. Display a transaction summary

### Basic Implementation
```cpp
// Question 1: Banking System
cout << "═══════════════════════════════════════" << endl;
cout << "    FTCC Federal Credit Union         " << endl;
cout << "═══════════════════════════════════════" << endl;

string accountName;
double startBalance, deposit, withdrawal;

cout << "Enter account holder name: ";
getline(cin, accountName);

cout << "Enter starting balance: $";
cin >> startBalance;

cout << "Enter deposit amount: $";
cin >> deposit;

cout << "Enter withdrawal amount: $";
cin >> withdrawal;

// Calculate final balance
double finalBalance = startBalance + deposit - withdrawal;

// Generate account number (example: use random or timestamp)
int accountNumber = 100000 + (rand() % 900000);

// Display summary
cout << "\n──── Transaction Summary ────" << endl;
cout << "Account: " << accountName << endl;
cout << "Account #: " << accountNumber << endl;
cout << "Final Balance: $" << finalBalance << endl;
```

### Suggested Improvements
- ✅ Handle full names with spaces using `getline()`
- ✅ Format currency with 2 decimal places using `setprecision(2)`
- ✅ Add overdraft warning if final balance is negative
- ✅ Show transaction history with timestamps

---

## Question 2: Crate Company Update

### The Scenario
Modify the General Crates program from M2LAB1 with new economic conditions.

### New Business Rules
- Storage cost increased to $0.35 per cubic foot (was $0.30)
- Maximum customer charge limited to $0.52 per cubic foot
- Labor costs remain at $0.10 per square foot

### Requirements
Update your M2LAB1 program with:
1. New cost constants
2. Profitability analysis
3. Warning if profit margin < 15%

### Key Changes
```cpp
const double COST_PER_CUBIC_FOOT = 0.35;    // Updated
const double CHARGE_PER_CUBIC_FOOT = 0.52;  // Maximum

// After calculating profit margin
if (profitMargin < 15) {
    cout << "⚠ WARNING: Low profit margin!" << endl;
    cout << "Consider larger crates or negotiating price." << endl;
}
```

### Suggested Improvements
- ✅ Format all money values with 2 decimal places
- ✅ Add break-even analysis
- ✅ Calculate minimum profitable crate size

---

## Question 3: Pizza Party Calculator

### The Scenario
You're organizing the Computer Science Club's end-of-semester pizza party. Create a calculator to ensure everyone gets enough pizza!

### Requirements
The program should:
1. Ask how many pizzas ordered
2. Ask slices per pizza
3. Ask number of visitors
4. Calculate leftover slices (each person gets 3 slices)

### Implementation
```cpp
// Question 3: Pizza Party Calculator
cout << "🍕 PIZZA PARTY PLANNER 🍕" << endl;
cout << "-------------------------" << endl;

int numPizzas, slicesPerPizza, numVisitors;
const int SLICES_PER_PERSON = 3;

cout << "How many pizzas are you ordering? ";
cin >> numPizzas;

cout << "How many slices per pizza? ";
cin >> slicesPerPizza;

cout << "How many visitors expected? ";
cin >> numVisitors;

// Calculations
int totalSlices = numPizzas * slicesPerPizza;
int slicesNeeded = numVisitors * SLICES_PER_PERSON;
int leftoverSlices = totalSlices - slicesNeeded;

// Display results
cout << "\n──── Party Summary ────" << endl;
cout << "Total slices available: " << totalSlices << endl;
cout << "Slices needed: " << slicesNeeded << endl;

if (leftoverSlices >= 0) {
    cout << "Leftover slices: " << leftoverSlices << endl;
} else {
    cout << "⚠ SHORT by " << abs(leftoverSlices) << " slices!" << endl;
    int extraPizzas = (abs(leftoverSlices) + slicesPerPizza - 1) / slicesPerPizza;
    cout << "Order " << extraPizzas << " more pizzas!" << endl;
}
```

### Suggested Improvements
- ✅ Handle different slice amounts per person
- ✅ Calculate cost with price per pizza
- ✅ Suggest optimal pizza order quantity

---

## Question 4: School Spirit Generator

### The Scenario
Create a customizable cheer generator for FTCC's sports teams.

### Requirements
Output this exact pattern:
```
Let's go FTCC
Let's go FTCC
Let's go FTCC
Let's go Trojans
```

Using ONLY these variables:
```cpp
string school = "FTCC";
string team = "Trojans";
```

### Basic Implementation
```cpp
// Question 4: School Spirit Generator
cout << "📣 SCHOOL SPIRIT GENERATOR 📣" << endl;
cout << "----------------------------" << endl;

string school = "FTCC";
string team = "Trojans";

// Basic output
cout << "Let's go " << school << endl;
cout << "Let's go " << school << endl;
cout << "Let's go " << school << endl;
cout << "Let's go " << team << endl;
```

### Advanced Challenge (Bonus Points)
**Constraints:**
- Cannot use raw strings in cout (no "Let's go")
- Must use string concatenation
- Only these variables allowed:
```cpp
string letsGo = "Let's go ";
string school = "FTCC";
string team = "Trojans";
string cheerOne, cheerTwo;

// Build cheers using concatenation
cheerOne = letsGo + school;
cheerTwo = letsGo + team;

// Output using only variables
cout << cheerOne << endl;
cout << cheerOne << endl;
cout << cheerOne << endl;
cout << cheerTwo << endl;
```

---

## Complete Program Template

```cpp
/*
    CSC 134
    M2HW1 - [Your Tier]
    [Your Name]
    [Date]
    
    Multi-program homework demonstrating:
    - User input with cin and getline
    - Calculations and formulas
    - Formatted output
    - String manipulation
*/

#include <iostream>
#include <iomanip>
#include <string>
#include <cstdlib>  // for rand()
#include <cmath>    // for abs()
using namespace std;

int main() {
    // Set currency formatting
    cout << fixed << setprecision(2);
    
    // Question 1: Banking System
    cout << "\n════════════════════════════════" << endl;
    cout << "  Question 1: Banking System    " << endl;
    cout << "════════════════════════════════" << endl;
    // [Your code here]
    
    // Question 2: Crate Company (if Silver/Gold)
    cout << "\n════════════════════════════════" << endl;
    cout << "  Question 2: Crate Company     " << endl;
    cout << "════════════════════════════════" << endl;
    // [Your code here]
    
    // Continue for other questions...
    
    return 0;
}
```

## Submission Requirements

1. **Source code:** `m2hw1_lastname.cpp` (or multiple files)
2. **Screenshots:** Output from each completed question
3. **Tier declaration:** Clearly state your target tier

## Grading Rubric

### Per Question (25 points each)
- **Functionality (15 pts):** Program works correctly
- **Code Quality (5 pts):** Clean, well-organized code
- **Output Format (5 pts):** Professional presentation

### Tier Bonuses
- Bronze: Maximum 80% (2 questions × 25 = 50/100 × 1.6 = 80)
- Silver: Maximum 90% (3 questions × 25 = 75/100 × 1.2 = 90)
- Gold: Maximum 100% (4 questions × 25 = 100)
- Diamond: Up to 110% (Gold + all improvements)

## Testing Checklist

### Question 1 (Banking)
- [ ] Handles names with spaces
- [ ] Negative balance warning
- [ ] Currency formatting

### Question 2 (Crates)
- [ ] New constants applied
- [ ] Profit margin calculated
- [ ] Low margin warning

### Question 3 (Pizza)
- [ ] Correct leftover calculation
- [ ] Shortage detection
- [ ] Additional pizza suggestion

### Question 4 (Spirit)
- [ ] Exact output format
- [ ] Uses required variables
- [ ] Bonus: String concatenation

## Common Mistakes to Avoid
- **Buffer issues:** Use `cin.ignore()` when mixing `cin >>` and `getline()`
- **Integer division:** Use doubles for money calculations
- **Missing labels:** Always identify which question you're answering
- **Wrong tier:** Declare your tier and complete the required number

## Why This Matters
This assignment demonstrates your ability to:
- Solve diverse real-world problems
- Choose appropriate data types
- Format professional output
- Manage program complexity
- Self-assess and target achievement levels

## Tips for Success
1. **Start with your strongest questions** to build confidence
2. **Test each question independently** before combining
3. **Save often** and keep backups
4. **Comment your code** to track your logic
5. **Ask for help early** if you're stuck

## Next Module Preview
Module 3 will introduce selection statements (if/else), allowing your programs to make decisions based on conditions. You'll upgrade these programs to be even smarter!