# M1HW1: Interactive Student Budget Analyzer

## The Scenario
The Financial Aid office has noticed that many students struggle with budget management during their first semester. They've commissioned you to create an interactive tool that helps students understand their financial situation. Your program will collect information about income and expenses, perform analysis, and provide actionable insights about their budget health.

This tool will be featured on the college website's student resources page, potentially helping hundreds of students avoid financial stress.

## Learning Objectives
By completing this assignment, you will:
- Implement user input with `cin` for various data types
- Combine multiple inputs with complex calculations
- Create a genuinely useful real-world application
- Handle user interaction professionally
- Provide data-driven insights through programming

## Background: The Student Budget Crisis
Recent surveys show:
- 70% of community college students work while studying
- Average student runs out of money 3 days before payday
- Most students don't know their actual monthly expenses
- Small daily purchases ($5 coffee) add up to significant amounts

Your tool will help students see the full picture of their finances.

## Part 1: Design and Planning (15 points)

### User Research
Your program must handle these common student scenarios:
1. Part-time worker + financial aid
2. Full-time worker + part-time student
3. Living with parents vs. independent
4. Seasonal income variation

### Input Categories to Track
- **Income:** Work, financial aid, family support, other
- **Fixed Expenses:** Tuition, rent, insurance, phone
- **Variable Expenses:** Food, gas, entertainment, supplies
- **Savings Goals:** Emergency fund, next semester, specific purchase

**Deliverable:** Comment block explaining your approach to each scenario

## Part 2: Core Implementation (50 points)

### Step 2.1: Program Structure
Create: `m1hw1_lastname.cpp`

```cpp
/*
    CSC 134
    M1HW1 - Student Budget Analyzer
    [Your Name]
    [Date]
    
    Interactive budget analysis tool for college students
    Provides personalized financial insights and recommendations
    
    Design Notes:
    - All money values stored as doubles for cent precision
    - Monthly basis for all calculations
    - Includes both required and optional expenses
*/

#include <iostream>
#include <iomanip>
#include <string>
using namespace std;

int main() {
    // Program header
    cout << "═══════════════════════════════════════════════════" << endl;
    cout << "     STUDENT BUDGET ANALYZER v1.0                  " << endl;
    cout << "     Financial Wellness for College Success        " << endl;
    cout << "═══════════════════════════════════════════════════" << endl;
    
    // User information
    string studentName;
    int creditHours;
    string livingSituation;  // "home" or "independent"
    
    // Your implementation continues here...
    
    return 0;
}
```

### Step 2.2: Collect User Information

Implement professional input gathering:

```cpp
// Get basic information
cout << "\nLet's analyze your budget. First, some basic info:" << endl;
cout << "Enter your first name: ";
cin >> studentName;

cout << "How many credit hours this semester? ";
cin >> creditHours;

cout << "Living situation (enter 'home' or 'independent'): ";
cin >> livingSituation;

// Income Section
cout << "\n──── MONTHLY INCOME ────" << endl;
cout << "Enter monthly work income (0 if not working): $";
double workIncome;
cin >> workIncome;

cout << "Enter monthly financial aid (after tuition): $";
double financialAid;
cin >> financialAid;

cout << "Enter family support amount: $";
double familySupport;
cin >> familySupport;

cout << "Enter other income (scholarships, etc.): $";
double otherIncome;
cin >> otherIncome;
```

### Step 2.3: Collect Expense Information

```cpp
// Fixed Expenses
cout << "\n──── FIXED MONTHLY EXPENSES ────" << endl;

double rent = 0;
if (livingSituation == "independent") {
    cout << "Enter monthly rent: $";
    cin >> rent;
}

cout << "Enter phone bill: $";
double phoneBill;
cin >> phoneBill;

cout << "Enter insurance (car/health/etc. total): $";
double insurance;
cin >> insurance;

cout << "Enter any loan payments: $";
double loanPayments;
cin >> loanPayments;

// Variable Expenses
cout << "\n──── VARIABLE MONTHLY EXPENSES ────" << endl;

cout << "Estimate monthly food/groceries: $";
double food;
cin >> food;

cout << "Estimate monthly gas/transportation: $";
double transportation;
cin >> transportation;

cout << "Estimate monthly entertainment: $";
double entertainment;
cin >> entertainment;

cout << "Estimate monthly school supplies: $";
double supplies;
cin >> supplies;

// Daily habit tracking
cout << "\n──── DAILY HABITS ────" << endl;
cout << "Average daily coffee/snack spending: $";
double dailySpending;
cin >> dailySpending;
```

### Step 2.4: Perform Analysis

```cpp
// Calculate totals
double totalIncome = workIncome + financialAid + familySupport + otherIncome;
double fixedExpenses = rent + phoneBill + insurance + loanPayments;
double variableExpenses = food + transportation + entertainment + supplies;
double monthlyDailySpending = dailySpending * 30;
double totalExpenses = fixedExpenses + variableExpenses + monthlyDailySpending;

// Calculate key metrics
double netIncome = totalIncome - totalExpenses;
double savingsRate = (netIncome / totalIncome) * 100;
double expenseRatio = (totalExpenses / totalIncome) * 100;

// Time-based calculations
double weeklyBudget = netIncome / 4.33;  // Average weeks per month
double dailyBudget = netIncome / 30;

// Semester projection (4 months)
double semesterBalance = netIncome * 4;

// Calculate "latte factor" - impact of daily spending
double yearlyDailyHabits = monthlyDailySpending * 12;
```

### Step 2.5: Generate Insights and Recommendations

```cpp
cout << "\n═══════════════════════════════════════════════════" << endl;
cout << "           BUDGET ANALYSIS RESULTS                  " << endl;
cout << "═══════════════════════════════════════════════════" << endl;

cout << fixed << setprecision(2);

// Summary Section
cout << "\n📊 MONTHLY SUMMARY FOR " << studentName << ":" << endl;
cout << "────────────────────────────────────" << endl;
cout << "Total Income:        $" << setw(10) << totalIncome << endl;
cout << "Total Expenses:      $" << setw(10) << totalExpenses << endl;
cout << "────────────────────────────────────" << endl;

if (netIncome >= 0) {
    cout << "Net Income:          $" << setw(10) << netIncome << " ✓" << endl;
} else {
    cout << "Net Income:         -$" << setw(10) << abs(netIncome) << " ⚠" << endl;
}

// Detailed Breakdown
cout << "\n📈 EXPENSE BREAKDOWN:" << endl;
cout << "Fixed Expenses:      $" << setw(10) << fixedExpenses 
     << " (" << (fixedExpenses/totalExpenses)*100 << "%)" << endl;
cout << "Variable Expenses:   $" << setw(10) << variableExpenses
     << " (" << (variableExpenses/totalExpenses)*100 << "%)" << endl;
cout << "Daily Habits:        $" << setw(10) << monthlyDailySpending
     << " (" << (monthlyDailySpending/totalExpenses)*100 << "%)" << endl;

// Budget Health Indicators
cout << "\n💰 FINANCIAL HEALTH INDICATORS:" << endl;
cout << "────────────────────────────────────" << endl;

string healthStatus;
if (savingsRate > 20) {
    healthStatus = "EXCELLENT";
} else if (savingsRate > 10) {
    healthStatus = "GOOD";
} else if (savingsRate > 0) {
    healthStatus = "FAIR";
} else {
    healthStatus = "NEEDS ATTENTION";
}

cout << "Budget Health: " << healthStatus << endl;
cout << "Savings Rate: " << savingsRate << "%" << endl;
cout << "Expense Ratio: " << expenseRatio << "%" << endl;

// Projections
cout << "\n🔮 PROJECTIONS:" << endl;
cout << "────────────────────────────────────" << endl;
cout << "Weekly Available:    $" << weeklyBudget << endl;
cout << "Daily Available:     $" << dailyBudget << endl;
cout << "Semester Savings:    $" << semesterBalance << endl;

// Smart Recommendations
cout << "\n💡 PERSONALIZED RECOMMENDATIONS:" << endl;
cout << "────────────────────────────────────" << endl;

// Recommendation 1: Daily spending impact
if (dailySpending > 5) {
    double potentialSavings = (dailySpending - 3) * 30;
    cout << "• Reducing daily purchases to $3 would save $" 
         << potentialSavings << "/month" << endl;
    cout << "  That's $" << potentialSavings * 12 << " per year!" << endl;
}

// Recommendation 2: Emergency fund
double emergencyFundTarget = totalExpenses * 3;  // 3 months expenses
if (netIncome > 0) {
    int monthsToEmergency = emergencyFundTarget / netIncome;
    cout << "• Build emergency fund of $" << emergencyFundTarget 
         << " in " << monthsToEmergency << " months" << endl;
}

// Recommendation 3: Credit hour cost awareness
double perCreditCost = totalExpenses / creditHours;
cout << "• Each credit hour costs you $" << perCreditCost 
     << " in living expenses" << endl;
cout << "  Make every class count!" << endl;

// Recommendation 4: Biggest expense category
if (entertainment > totalExpenses * 0.15) {
    cout << "• Entertainment is " << (entertainment/totalExpenses)*100 
         << "% of budget (recommended: <15%)" << endl;
}

// Warning for negative budget
if (netIncome < 0) {
    cout << "\n⚠️  WARNING: Expenses exceed income by $" 
         << abs(netIncome) << endl;
    cout << "   Consider: Part-time work, reduce expenses, or financial aid" << endl;
}
```

## Part 3: Advanced Features (25 points)

### Required Feature: Savings Goal Calculator
```cpp
cout << "\n📌 SAVINGS GOAL PLANNER:" << endl;
cout << "────────────────────────────────────" << endl;
cout << "Enter your savings goal amount: $";
double goalAmount;
cin >> goalAmount;

cout << "Enter target date (months from now): ";
int targetMonths;
cin >> targetMonths;

double monthlyRequired = goalAmount / targetMonths;

cout << "\nTo save $" << goalAmount << " in " << targetMonths << " months:" << endl;
cout << "Required monthly savings: $" << monthlyRequired << endl;

if (monthlyRequired <= netIncome) {
    cout << "✓ This goal is achievable with your current budget!" << endl;
    double remaining = netIncome - monthlyRequired;
    cout << "  You'll have $" << remaining << " left for other purposes." << endl;
} else {
    double shortfall = monthlyRequired - netIncome;
    cout << "⚠ You need $" << shortfall << " more per month." << endl;
    cout << "  Consider reducing expenses or increasing income." << endl;
}
```

### Optional Enhancement (Choose ONE for bonus):

**Option A: Debt Payoff Calculator (+5 points)**
Calculate how long to pay off credit card or loan

**Option B: Side Hustle Analyzer (+5 points)**
Show impact of adding 10 hours/week of work

**Option C: Scholarship ROI Calculator (+5 points)**
Show time investment vs. financial return for scholarship applications

## Part 4: Professional Polish (10 points)

### Error Handling
Add basic input validation:
```cpp
if (totalIncome <= 0) {
    cout << "Error: Income must be greater than 0" << endl;
    return 1;
}
```

### Visual Enhancement
Use ASCII art or Unicode characters to make output more engaging:
```cpp
cout << "┌─────────────────────────────┐" << endl;
cout << "│   YOUR FINANCIAL SNAPSHOT   │" << endl;
cout << "└─────────────────────────────┘" << endl;
```

## Submission Requirements

1. **Source code:** `m1hw1_lastname.cpp`
2. **Test run screenshot:** Complete program execution
3. **Reflection document:** 1-page reflection on what you learned
4. **GitHub link:** To your committed file

## Grading Rubric (100 points)

### Design and Planning (15 points)
- **Excellent (14-15):** Thoughtful design, all scenarios considered
- **Good (12-13):** Good planning, most cases handled
- **Satisfactory (10-11):** Basic planning present
- **Needs Improvement (0-9):** Minimal planning

### Core Implementation (35 points)
- **Excellent (33-35):** All features work perfectly, clean code
- **Good (28-32):** Most features work, good code structure
- **Satisfactory (23-27):** Basic functionality works
- **Needs Improvement (0-22):** Major issues or missing features

### Calculations and Analysis (25 points)
- **Excellent (23-25):** All calculations correct, insightful analysis
- **Good (20-22):** Most calculations correct, good analysis
- **Satisfactory (17-19):** Basic calculations work
- **Needs Improvement (0-16):** Calculation errors or missing analysis

### User Interaction (15 points)
- **Excellent (14-15):** Clear prompts, professional interaction
- **Good (12-13):** Good prompts, mostly clear
- **Satisfactory (10-11):** Basic interaction works
- **Needs Improvement (0-9):** Confusing or poor interaction

### Professional Polish (10 points)
- **Excellent (9-10):** Error handling, visual appeal, extra features
- **Good (7-8):** Some polish, attempts at enhancement
- **Satisfactory (5-6):** Basic requirements met
- **Needs Improvement (0-4):** Minimal effort on polish

## Testing Scenarios

Test your program with these cases:

### Scenario 1: The Struggling Student
- Income: $800/month (part-time)
- Expenses: $950/month
- Should trigger warnings and suggestions

### Scenario 2: The Saver
- Income: $2000/month
- Expenses: $1200/month  
- Should show strong financial health

### Scenario 3: The Break-Even Student
- Income: $1500/month
- Expenses: $1480/month
- Should suggest ways to increase savings

## Common Issues and Solutions

### Input Type Mismatches
**Problem:** Program crashes when user enters text for number
**Solution:** Will be covered in Module 3 (input validation)
**For now:** Tell users to enter numbers only

### Negative Numbers
**Problem:** User enters negative expenses
**Solution:** Add simple checks after input

### Division by Zero
**Problem:** Calculating percentages when income is 0
**Solution:** Check for zero before division

## Why This Assignment Matters

This program demonstrates how programming can solve real personal problems. The skills you're developing:
- **User interaction design** - Making programs people want to use
- **Data analysis** - Turning numbers into insights  
- **Problem solving** - Addressing real-world needs
- **Financial literacy** - Understanding budget concepts

These exact skills are used in:
- Banking applications
- Financial planning software
- Business intelligence tools
- Personal finance apps

## Reflection Questions

1. How did getting user input change your program design approach?
2. What was the most challenging calculation to implement?
3. How could this program be improved for real-world use?
4. What did you learn about your own budget while testing?

## Next Module Preview
In Module 2, you'll learn about selection statements (if/else), allowing your programs to make decisions based on conditions. You'll upgrade this budget analyzer to provide even smarter, more personalized recommendations.

## Final Thoughts
You've just built a genuinely useful tool that could help real students manage their finances better. Be proud of this accomplishment! Consider actually using this tool for your own budget planning.

Remember: The best programs solve real problems for real people.