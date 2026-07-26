# M2LAB1: General Crates Manufacturing Case Study

## The Scenario
General Crates, Inc. manufactures custom wooden shipping crates for industrial clients. They've hired you to create a cost analysis program that their sales team can use to quickly quote prices to customers. The program needs to calculate material costs, labor, and determine profit margins based on crate dimensions that customers request.

This is a real business problem - accurate pricing is critical for profitability!

## Learning Objectives
By completing this lab, you will:
- Solve a multi-step business problem
- Work with volume calculations (3D geometry)
- Calculate costs, charges, and profit margins
- Create a professional business report output
- Practice problem decomposition and pseudocode

## Background: The Business Model
General Crates' pricing model:
- **Material Cost:** Based on cubic feet of wood needed
- **Labor Cost:** Based on surface area (more area = more assembly time)
- **Customer Charge:** Based on crate volume (cubic feet)
- **Profit:** Difference between charge and total costs

Understanding the business before coding is essential!

## Part 1: Problem Analysis (20 points)

### Step 1.1: Do It By Hand First
Before coding, calculate manually for a crate that is:
- Length: 10 feet
- Width: 8 feet  
- Height: 4 feet

Calculate:
1. Volume (cubic feet)
2. Surface area (square feet)
3. Material cost at $0.30 per cubic foot
4. Labor cost at $0.10 per square foot of surface
5. Customer charge at $0.52 per cubic foot
6. Profit (charge - all costs)

**Deliverable:** Include hand calculations as comments

### Step 1.2: Create Pseudocode
Write pseudocode outlining your program flow:
```
// Get crate dimensions from user
// Calculate volume
// Calculate surface area
// Calculate costs
// Calculate charge
// Calculate profit
// Display report
```

## Part 2: Implementation (50 points)

### Step 2.1: Create Your Program File
Create: `m2lab1_lastname.cpp`

### Step 2.2: Professional Header
```cpp
/*
    CSC 134
    M2LAB1 - Crate Manufacturing Cost Analysis
    [Your Name]
    [Date]
    
    Cost analysis system for General Crates, Inc.
    Calculates material costs, labor, and profit margins
    for custom crate manufacturing.
    
    Business Rules:
    - Material cost: $0.30 per cubic foot
    - Labor cost: $0.10 per square foot of surface
    - Customer charge: $0.52 per cubic foot
    
    Hand Calculation Verification (10 x 8 x 4 crate):
    [Your calculations here]
*/
```

### Step 2.3: Core Program Structure

```cpp
#include <iostream>
#include <iomanip>
#include <string>
using namespace std;

int main() {
    // Company header
    cout << "═══════════════════════════════════════════" << endl;
    cout << "       GENERAL CRATES, INC.                " << endl;
    cout << "    Cost Analysis System v2.0              " << endl;
    cout << "═══════════════════════════════════════════" << endl;
    cout << endl;
    
    // Constants for business rules
    const double COST_PER_CUBIC_FOOT = 0.30;    // Material cost
    const double LABOR_PER_SQ_FOOT = 0.10;      // Labor cost
    const double CHARGE_PER_CUBIC_FOOT = 0.52;  // Customer charge
    
    // Get customer information
    string customerName;
    string companyName;
    
    cout << "CUSTOMER INFORMATION" << endl;
    cout << "-------------------" << endl;
    cout << "Customer name: ";
    getline(cin, customerName);
    cout << "Company name: ";
    getline(cin, companyName);
    cout << endl;
    
    // Get crate specifications
    double length, width, height;
    
    cout << "CRATE SPECIFICATIONS" << endl;
    cout << "-------------------" << endl;
    cout << "Enter crate length (feet): ";
    cin >> length;
    cout << "Enter crate width (feet): ";
    cin >> width;
    cout << "Enter crate height (feet): ";
    cin >> height;
    
    // Calculate volume and surface area
    double volume = length * width * height;
    
    // Surface area = 2(lw + lh + wh)
    double surfaceArea = 2 * (length * width + 
                             length * height + 
                             width * height);
    
    // Calculate costs
    double materialCost = volume * COST_PER_CUBIC_FOOT;
    double laborCost = surfaceArea * LABOR_PER_SQ_FOOT;
    double totalCost = materialCost + laborCost;
    
    // Calculate customer charge
    double customerCharge = volume * CHARGE_PER_CUBIC_FOOT;
    
    // Calculate profit
    double profit = customerCharge - totalCost;
    double profitMargin = (profit / customerCharge) * 100;
    
    // Format for currency
    cout << fixed << setprecision(2);
    
    // Display cost analysis report
    cout << "\n╔═══════════════════════════════════════════╗" << endl;
    cout << "║         COST ANALYSIS REPORT              ║" << endl;
    cout << "╠═══════════════════════════════════════════╣" << endl;
    cout << "║ Customer: " << left << setw(32) << customerName << "║" << endl;
    cout << "║ Company:  " << left << setw(32) << companyName << "║" << endl;
    cout << "╠═══════════════════════════════════════════╣" << endl;
    cout << "║ CRATE DIMENSIONS                          ║" << endl;
    cout << "║   Length: " << setw(8) << length << " ft                    ║" << endl;
    cout << "║   Width:  " << setw(8) << width << " ft                    ║" << endl;
    cout << "║   Height: " << setw(8) << height << " ft                    ║" << endl;
    cout << "║                                           ║" << endl;
    cout << "║ CALCULATED VALUES                         ║" << endl;
    cout << "║   Volume:       " << setw(10) << volume << " cubic ft    ║" << endl;
    cout << "║   Surface Area: " << setw(10) << surfaceArea << " sq ft       ║" << endl;
    cout << "╠═══════════════════════════════════════════╣" << endl;
    cout << "║ COST BREAKDOWN                            ║" << endl;
    cout << "║   Material Cost:  $" << setw(10) << materialCost << "         ║" << endl;
    cout << "║   Labor Cost:     $" << setw(10) << laborCost << "         ║" << endl;
    cout << "║   ─────────────────────────               ║" << endl;
    cout << "║   Total Cost:     $" << setw(10) << totalCost << "         ║" << endl;
    cout << "╠═══════════════════════════════════════════╣" << endl;
    cout << "║ PRICING                                   ║" << endl;
    cout << "║   Customer Price: $" << setw(10) << customerCharge << "         ║" << endl;
    cout << "║   Profit:         $" << setw(10) << profit << "         ║" << endl;
    cout << "║   Profit Margin:   " << setw(10) << profitMargin << "%        ║" << endl;
    cout << "╚═══════════════════════════════════════════╝" << endl;
    
    // Add recommendations based on profit margin
    cout << "\nRECOMMENDATION: ";
    if (profitMargin < 20) {
        cout << "⚠ Low profit margin. Consider negotiating price." << endl;
    } else if (profitMargin < 30) {
        cout << "✓ Acceptable profit margin." << endl;
    } else {
        cout << "✓ Excellent profit margin!" << endl;
    }
    
    // Add bulk order option
    cout << "\nBULK ORDER ANALYSIS" << endl;
    cout << "-------------------" << endl;
    cout << "How many crates does the customer need? ";
    int quantity;
    cin >> quantity;
    
    double bulkTotal = customerCharge * quantity;
    double bulkProfit = profit * quantity;
    
    cout << "\nBulk Order Summary:" << endl;
    cout << "  " << quantity << " crates @ $" << customerCharge << " each" << endl;
    cout << "  Total Revenue: $" << bulkTotal << endl;
    cout << "  Total Profit:  $" << bulkProfit << endl;
    
    return 0;
}
```

## Part 3: Business Analysis (30 points)

### Economic Fluctuation Scenario
The market has changed! Update your program with new rates:
- Material cost increases to $0.35 per cubic foot
- Labor remains at $0.10 per square foot
- Maximum charge customers will accept: $0.52 per cubic foot

### Analysis Questions
1. How does this affect profit margins?
2. What's the minimum crate size for profitability?
3. Should General Crates focus on larger or smaller crates?

Document your findings in comments.

## Submission Requirements

1. **Source code:** `m2lab1_lastname.cpp`
2. **Test runs:** Screenshots with 3 different crate sizes
3. **Analysis:** Written answers to business questions

## Grading Rubric (100 points)

### Problem Analysis (20 points)
- **Excellent (18-20):** Complete hand calculations and pseudocode
- **Good (15-17):** Most calculations shown, good pseudocode
- **Satisfactory (12-14):** Basic analysis present
- **Needs Improvement (0-11):** Minimal analysis

### Implementation (40 points)
- **Excellent (37-40):** All calculations correct, clean code
- **Good (32-36):** Most features work, good structure
- **Satisfactory (26-31):** Basic functionality
- **Needs Improvement (0-25):** Major issues

### Output Formatting (20 points)
- **Excellent (18-20):** Professional report format
- **Good (15-17):** Good formatting, minor issues
- **Satisfactory (12-14):** Acceptable output
- **Needs Improvement (0-11):** Poor formatting

### Business Analysis (20 points)
- **Excellent (18-20):** Insightful analysis with evidence
- **Good (15-17):** Good analysis, understands impact
- **Satisfactory (12-14):** Basic analysis
- **Needs Improvement (0-11):** Minimal analysis

## Sample Output
```
═══════════════════════════════════════════
       GENERAL CRATES, INC.                
    Cost Analysis System v2.0              
═══════════════════════════════════════════

CUSTOMER INFORMATION
-------------------
Customer name: John Smith
Company name: Smith Industries

CRATE SPECIFICATIONS
-------------------
Enter crate length (feet): 10
Enter crate width (feet): 8
Enter crate height (feet): 4

╔═══════════════════════════════════════════╗
║         COST ANALYSIS REPORT              ║
╠═══════════════════════════════════════════╣
║ Customer: John Smith                      ║
║ Company:  Smith Industries                ║
╠═══════════════════════════════════════════╣
║ CRATE DIMENSIONS                          ║
║   Length: 10.00     ft                    ║
║   Width:  8.00      ft                    ║
║   Height: 4.00      ft                    ║
║                                           ║
║ CALCULATED VALUES                         ║
║   Volume:       320.00     cubic ft       ║
║   Surface Area: 304.00     sq ft          ║
╠═══════════════════════════════════════════╣
║ COST BREAKDOWN                            ║
║   Material Cost:  $     96.00             ║
║   Labor Cost:     $     30.40             ║
║   ─────────────────────────               ║
║   Total Cost:     $    126.40             ║
╠═══════════════════════════════════════════╣
║ PRICING                                   ║
║   Customer Price: $    166.40             ║
║   Profit:         $     40.00             ║
║   Profit Margin:       24.04%             ║
╚═══════════════════════════════════════════╝

RECOMMENDATION: ✓ Acceptable profit margin.
```

## Common Mistakes to Avoid
- **Formula errors:** Surface area requires all 6 faces
- **Unit confusion:** Everything should be in feet
- **Missing costs:** Don't forget both material AND labor
- **Integer division:** Use doubles for all measurements

## Why This Matters
This case study mirrors real business software development. Companies rely on accurate cost analysis for:
- Pricing decisions
- Profitability analysis
- Competitive positioning
- Resource planning

The skills you're learning apply directly to:
- Manufacturing systems
- Construction estimating
- Logistics planning
- Any business with cost/revenue calculations

## Next Steps
M2HW1 will combine multiple programs including banking, event planning, and string manipulation, bringing together all Module 2 concepts.