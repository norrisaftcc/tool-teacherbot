# M2T2: The Smart Restaurant Bill Calculator

## The Scenario
You've been hired by "The Binary Bite," a new tech-themed restaurant near campus, to create an interactive bill calculator for their servers' tablets. The restaurant wants to make bill splitting and tipping easier for their customers, especially student groups who often need to split checks. Your calculator will help servers quickly show customers their total with various tip options.

## Learning Objectives
By completing this assignment, you will:
- Perform percentage calculations (tax and tip)
- Format currency output with proper decimal places
- Create a user-friendly calculator interface
- Use `iomanip` for professional formatting
- Handle multiple calculation steps in sequence

## Background: Restaurant Math
Restaurant bills involve several calculations:
1. **Subtotal**: Sum of all food and drink prices
2. **Tax**: Percentage of subtotal (varies by location)
3. **Tip**: Percentage of subtotal (varies by service)
4. **Total**: Subtotal + Tax + Tip

The order matters! Some people tip on the pre-tax amount, others on post-tax.

## Part 1: Understanding the Requirements (15 points)

### Restaurant Specifications
The Binary Bite has provided these requirements:
- Sales tax is 8% in your area
- Suggested tip amounts: 15%, 18%, 20%, 25%
- Bills often split between 1-6 people
- Students get a 10% discount with valid ID

### Planning Your Calculator
Before coding, determine:
1. What order to request information
2. Whether to tip on pre-tax or post-tax amount
3. How to display multiple tip options clearly

**Deliverable:** Include your design decisions as comments

## Part 2: Building the Bill Calculator (60 points)

### Step 2.1: Create Your Program File
Create: `m2t2_lastname.cpp`

### Step 2.2: Professional Header
```cpp
/*
    CSC 134
    M2T2 - Restaurant Bill Calculator
    [Your Name]
    [Date]
    
    Interactive bill calculator for The Binary Bite restaurant
    Calculates tax, offers tip suggestions, and splits bills
    
    Design Decisions:
    - Tax calculated on subtotal
    - Tip calculated on pre-tax amount (industry standard)
    - Shows multiple tip options for customer choice
*/
```

### Step 2.3: Implement the Calculator

```cpp
#include <iostream>
#include <iomanip>
#include <string>
using namespace std;

int main() {
    // Restaurant branding
    cout << "╔════════════════════════════════════╗" << endl;
    cout << "║        THE BINARY BITE             ║" << endl;
    cout << "║      Bill Calculator v2.0          ║" << endl;
    cout << "╚════════════════════════════════════╝" << endl;
    cout << endl;
    
    // Get server name for personalization
    string serverName;
    cout << "Server name: ";
    getline(cin, serverName);
    
    // Get meal information
    double mealCost;
    cout << "\nEnter the meal subtotal: $";
    cin >> mealCost;
    
    // Check for student discount
    char hasStudentID;
    cout << "Does customer have student ID? (y/n): ";
    cin >> hasStudentID;
    
    double discount = 0;
    if (hasStudentID == 'y' || hasStudentID == 'Y') {
        discount = mealCost * 0.10;
        cout << "10% student discount applied!" << endl;
    }
    
    // Apply discount to get final subtotal
    double subtotal = mealCost - discount;
    
    // Calculate tax
    const double TAX_RATE = 0.08;
    double taxAmount = subtotal * TAX_RATE;
    double afterTax = subtotal + taxAmount;
    
    // Set up currency formatting
    cout << fixed << setprecision(2);
    
    // Display initial bill breakdown
    cout << "\n┌─────────────────────────────────┐" << endl;
    cout << "│         BILL BREAKDOWN          │" << endl;
    cout << "├─────────────────────────────────┤" << endl;
    cout << "│ Original:        $" << setw(10) << mealCost << " │" << endl;
    
    if (discount > 0) {
        cout << "│ Student Discount:-$" << setw(10) << discount << " │" << endl;
        cout << "│ Subtotal:        $" << setw(10) << subtotal << " │" << endl;
    }
    
    cout << "│ Tax (8%):        $" << setw(10) << taxAmount << " │" << endl;
    cout << "│ After Tax:       $" << setw(10) << afterTax << " │" << endl;
    cout << "└─────────────────────────────────┘" << endl;
    
    // Calculate tip options (on pre-tax amount)
    cout << "\n┌─────────────────────────────────┐" << endl;
    cout << "│      TIP SUGGESTIONS            │" << endl;
    cout << "├─────────────────────────────────┤" << endl;
    
    // Tip percentages
    double tips[] = {0.15, 0.18, 0.20, 0.25};
    string tipLabels[] = {"15% (Fair)", "18% (Good)", "20% (Great)", "25% (Excellent)"};
    
    for (int i = 0; i < 4; i++) {
        double tipAmount = subtotal * tips[i];
        double total = afterTax + tipAmount;
        cout << "│ " << left << setw(15) << tipLabels[i] 
             << "$" << right << setw(6) << tipAmount 
             << " = $" << setw(7) << total << " │" << endl;
    }
    cout << "└─────────────────────────────────┘" << endl;
    
    // Get actual tip amount
    double tipPercent;
    cout << "\nEnter tip percentage (e.g., 18 for 18%): ";
    cin >> tipPercent;
    
    double tipAmount = subtotal * (tipPercent / 100);
    double finalTotal = afterTax + tipAmount;
    
    // Ask about bill splitting
    int numPeople;
    cout << "Split bill? Enter number of people (1 for no split): ";
    cin >> numPeople;
    
    // Display final receipt
    cout << "\n╔════════════════════════════════════╗" << endl;
    cout << "║           FINAL RECEIPT            ║" << endl;
    cout << "╠════════════════════════════════════╣" << endl;
    cout << "║ Server: " << left << setw(27) << serverName << "║" << endl;
    cout << "╠════════════════════════════════════╣" << endl;
    cout << "║ Subtotal:        $" << right << setw(10) << subtotal << "   ║" << endl;
    cout << "║ Tax:             $" << setw(10) << taxAmount << "   ║" << endl;
    cout << "║ Tip (" << setw(2) << (int)tipPercent << "%):       $" 
         << setw(10) << tipAmount << "   ║" << endl;
    cout << "╠════════════════════════════════════╣" << endl;
    cout << "║ TOTAL:           $" << setw(10) << finalTotal << "   ║" << endl;
    
    if (numPeople > 1) {
        double perPerson = finalTotal / numPeople;
        cout << "╠════════════════════════════════════╣" << endl;
        cout << "║ Split " << numPeople << " ways:    $" 
             << setw(10) << perPerson << "   ║" << endl;
        cout << "║              per person            ║" << endl;
    }
    
    cout << "╚════════════════════════════════════╝" << endl;
    
    // Thank you message
    cout << "\n    Thank you for dining at" << endl;
    cout << "       The Binary Bite!" << endl;
    cout << "    01010100 01101000 01111000!" << endl;  // "Thx" in binary
    
    return 0;
}
```

### Step 2.4: Advanced Formatting Techniques

Learn these formatting tools:
```cpp
// Set decimal places for currency
cout << fixed << setprecision(2);

// Set field width for alignment
cout << setw(10) << value;

// Align text
cout << left << text;    // Left-align
cout << right << number;  // Right-align
```

## Part 3: Testing and Edge Cases (25 points)

### Test Scenarios
1. **No discount:** Customer without student ID
2. **With discount:** Student with ID
3. **No tip:** Enter 0 for tip percentage
4. **Large group:** Split 6 ways
5. **Solo diner:** Split 1 way (no split)

### Document Your Testing
Create a test table showing:
- Input values
- Expected output
- Actual output
- Pass/Fail

## Submission Requirements

1. **Source code:** `m2t2_lastname.cpp`
2. **Screenshots:** At least 3 different scenarios
3. **Test documentation:** Your test table

## Grading Rubric (100 points)

### Design and Planning (15 points)
- **Excellent (14-15):** Clear design decisions documented
- **Good (12-13):** Good planning evident
- **Satisfactory (10-11):** Basic planning present
- **Needs Improvement (0-9):** Minimal planning

### Calculation Accuracy (30 points)
- **Excellent (28-30):** All calculations correct
- **Good (24-27):** Most calculations correct
- **Satisfactory (20-23):** Basic calculations work
- **Needs Improvement (0-19):** Calculation errors

### Formatting and Presentation (30 points)
- **Excellent (28-30):** Professional formatting, perfect alignment
- **Good (24-27):** Good formatting, minor issues
- **Satisfactory (20-23):** Acceptable formatting
- **Needs Improvement (0-19):** Poor formatting

### Testing and Documentation (25 points)
- **Excellent (23-25):** Comprehensive testing documented
- **Good (20-22):** Good testing, most cases covered
- **Satisfactory (17-19):** Basic testing performed
- **Needs Improvement (0-16):** Minimal testing

## Sample Output
```
╔════════════════════════════════════╗
║        THE BINARY BITE             ║
║      Bill Calculator v2.0          ║
╚════════════════════════════════════╝

Server name: Alex Johnson

Enter the meal subtotal: $45.50
Does customer have student ID? (y/n): y
10% student discount applied!

┌─────────────────────────────────┐
│         BILL BREAKDOWN          │
├─────────────────────────────────┤
│ Original:        $     45.50 │
│ Student Discount:-$      4.55 │
│ Subtotal:        $     40.95 │
│ Tax (8%):        $      3.28 │
│ After Tax:       $     44.23 │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│      TIP SUGGESTIONS            │
├─────────────────────────────────┤
│ 15% (Fair)     $  6.14 = $  50.37 │
│ 18% (Good)     $  7.37 = $  51.60 │
│ 20% (Great)    $  8.19 = $  52.42 │
│ 25% (Excellent)$ 10.24 = $  54.47 │
└─────────────────────────────────┘

Enter tip percentage (e.g., 18 for 18%): 20
Split bill? Enter number of people (1 for no split): 2

╔════════════════════════════════════╗
║           FINAL RECEIPT            ║
╠════════════════════════════════════╣
║ Server: Alex Johnson               ║
╠════════════════════════════════════╣
║ Subtotal:        $     40.95   ║
║ Tax:             $      3.28   ║
║ Tip (20%):       $      8.19   ║
╠════════════════════════════════════╣
║ TOTAL:           $     52.42   ║
╠════════════════════════════════════╣
║ Split 2 ways:    $     26.21   ║
║              per person            ║
╚════════════════════════════════════╝

    Thank you for dining at
       The Binary Bite!
    01010100 01101000 01111000!
```

## Common Mistakes to Avoid
- **Wrong calculation order:** Tax before discount
- **Tipping on wrong amount:** Should tip on pre-tax
- **Poor alignment:** Use `setw()` properly
- **Missing currency format:** Always use `fixed` and `setprecision(2)`

## Extension Challenges (Optional Bonus)

### Challenge 1: Custom Tip (+5 points)
Allow custom tip amounts beyond the suggestions

### Challenge 2: Item Entry (+5 points)
Let server enter individual items instead of just total

### Challenge 3: Happy Hour (+5 points)
Apply time-based discounts (happy hour pricing)

## Why This Matters
This calculator demonstrates real-world application development. Restaurant POS systems, payment apps, and e-commerce sites all need accurate financial calculations with clear presentation. You're learning to handle money in code - a critical skill where errors can cost real dollars.

## Key Concepts Reinforced
- **Percentage calculations:** Essential for finance applications
- **Formatting:** Professional presentation matters
- **User flow:** Logical order of operations
- **Testing:** Financial software must be accurate

## Next Steps
In M2LAB1, you'll tackle a more complex business case study involving manufacturing calculations, building on these formatting and calculation skills.