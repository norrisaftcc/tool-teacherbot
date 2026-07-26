# M1T2: Your Digital Business Card

## The Scenario
Your college career center is hosting a virtual networking event next week. They've asked all computer science students to create digital business cards that can be displayed on the event screens. Your card needs to present your professional information in a clean, organized format using a C++ program. This is your chance to make a great first impression on potential employers and internship coordinators!

## Learning Objectives
By completing this assignment, you will:
- Declare and initialize variables of different data types (string, int, double)
- Use variables to store and display information
- Format output for professional presentation
- Practice escape sequences for special characters
- Build on your Git workflow with meaningful commits

## Background: Variables as Information Containers
In programming, variables are like labeled boxes that hold information. Just like a business card has specific fields (name, title, contact), our program will use variables to store and organize your professional information.

```cpp
string name = "Jane Developer";        // Text information
int graduationYear = 2026;            // Whole numbers
double gpa = 3.75;                    // Numbers with decimals
```

## Part 1: Planning Your Business Card (15 points)

### What Makes a Good Digital Business Card?
Before coding, plan what information you'll display:
- Your professional name
- Your major/program
- Expected graduation year
- A professional tagline or objective
- Contact method (GitHub username or LinkedIn)
- One unique skill or interest

**Deliverable:** Include a comment block in your code with your planned information.

## Part 2: Building Your Digital Business Card (60 points)

### Step 2.1: Create Your Program File
Create a new file: `m1t2_lastname.cpp`

### Step 2.2: Professional Header and Planning
```cpp
/*
    CSC 134
    M1T2 - Digital Business Card
    [Your Name]
    [Date]
    
    This program creates a professional digital business card
    for networking events and portfolio presentations.
    
    Planning Notes:
    - Name: [Your professional name]
    - Program: [Your major]
    - Graduation: [Year]
    - Focus: [Your career interest]
    - Contact: [GitHub or LinkedIn]
    - Unique Factor: [Something memorable]
*/
```

### Step 2.3: Implement Your Business Card

Your program must include:

1. **At least 5 different variables:**
   - Minimum 2 string variables
   - Minimum 1 int variable  
   - Minimum 1 double variable
   - At least 1 additional variable of your choice

2. **Professional formatting with borders:**
```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    // Declare your variables
    string fullName = "Your Name";
    string major = "Computer Science";
    int gradYear = 2026;
    double completedCredits = 45.5;
    string githubUsername = "yourusername";
    string tagline = "Passionate about solving problems with code";
    
    // Display your business card
    cout << "╔═══════════════════════════════════════════════╗" << endl;
    cout << "║          DIGITAL BUSINESS CARD                ║" << endl;
    cout << "╠═══════════════════════════════════════════════╣" << endl;
    // Your formatted information here
    cout << "╚═══════════════════════════════════════════════╝" << endl;
    
    return 0;
}
```

3. **Required Output Elements:**
   - A decorative border (you can use simple characters like =, -, *, or # if the Unicode boxes don't work)
   - Your name prominently displayed
   - Your academic program and graduation year
   - At least one calculated or derived value (e.g., "Years until graduation: 2")
   - A professional tagline or career objective
   - Contact information

### Step 2.4: Add a Calculated Element
Include at least one calculation, such as:
- Years until graduation
- Percentage of degree completed
- Credits remaining
- Age at graduation

Example:
```cpp
int currentYear = 2024;
int yearsLeft = gradYear - currentYear;
cout << "║ Graduating in: " << yearsLeft << " years" << endl;
```

## Part 3: Professional Polish (25 points)

### Step 3.1: Special Formatting Challenge
Use at least TWO of the following:
- Tab characters (`\t`) for alignment
- Quotation marks in output using `\"`
- Special Unicode characters (♦ ▸ ★ ◆)
- Color codes (research ANSI escape codes - optional bonus)

### Step 3.2: Make It Memorable
Add one creative element that makes your card stand out:
- An ASCII art logo
- A motivational quote
- A "fun fact" about yourself
- A skill progress bar

Example progress bar:
```cpp
cout << "║ C++ Skills:    [████████░░] 80%              ║" << endl;
```

### Step 3.3: Test and Refine
1. Compile with all warnings enabled:
   ```bash
   g++ -std=c++17 -Wall -Wextra m1t2_lastname.cpp -o m1t2_lastname
   ```
2. Run multiple times to ensure consistent formatting
3. Have a friend review your output for professionalism

## Part 4: Git Workflow

### Meaningful Commits
Make at least TWO commits:
1. First commit after basic structure is working
2. Second commit after adding polish and creativity

Example commit messages:
```bash
git add m1t2_lastname.cpp
git commit -m "Add basic digital business card structure

- Implement required variables
- Create formatted output
- Add border design"

# After improvements:
git commit -m "Enhance business card with professional polish

- Add calculated graduation timeline
- Include skill progress indicators
- Improve visual formatting"
```

## Submission Requirements

1. **GitHub Link:** Direct link to your file
2. **Screenshot:** Your business card output in the terminal
3. **Reflection:** One paragraph (3-5 sentences) about what you learned

## Grading Rubric (100 points)

### Planning and Design (15 points)
- **Excellent (14-15):** Clear planning notes, professional information chosen
- **Good (12-13):** Good planning, most elements considered
- **Satisfactory (10-11):** Basic planning present
- **Needs Improvement (0-9):** Minimal or no planning

### Variable Implementation (30 points)
- **Excellent (28-30):** All required variables used effectively, good naming
- **Good (24-27):** Required variables present, mostly well-used
- **Satisfactory (20-23):** Basic variable usage, some issues
- **Needs Improvement (0-19):** Missing variables or incorrect usage

### Output and Formatting (30 points)
- **Excellent (28-30):** Professional appearance, all elements present, creative
- **Good (24-27):** Good formatting, most elements included
- **Satisfactory (20-23):** Basic formatting, acceptable output
- **Needs Improvement (0-19):** Poor formatting or missing elements

### Professional Polish (15 points)
- **Excellent (14-15):** Special formatting used well, memorable element included
- **Good (12-13):** Some special formatting, attempt at creativity
- **Satisfactory (10-11):** Basic requirements met
- **Needs Improvement (0-9):** Minimal effort on polish

### Git Workflow (10 points)
- **Excellent (9-10):** Multiple meaningful commits with good messages
- **Good (7-8):** Required commits made, decent messages
- **Satisfactory (5-6):** Basic Git usage
- **Needs Improvement (0-4):** Poor or missing Git workflow

## Sample Output
```
╔═══════════════════════════════════════════════╗
║          DIGITAL BUSINESS CARD                ║
╠═══════════════════════════════════════════════╣
║                                               ║
║  Jane Developer                               ║
║  Computer Science Major                       ║
║  Forsyth Technical Community College          ║
║                                               ║
║  Expected Graduation: 2026                    ║
║  ▸ 2 years remaining                          ║
║  ▸ 45.5 credits completed (50.6%)             ║
║                                               ║
║  "Turning coffee into code since 2024"        ║
║                                               ║
║  Skills in Development:                       ║
║  C++:      [████████░░] 80%                   ║
║  Python:   [██████░░░░] 60%                   ║
║  Git:      [█████████░] 90%                   ║
║                                               ║
║  Connect: github.com/janedev                  ║
║                                               ║
╚═══════════════════════════════════════════════╝
```

## Common Mistakes to Avoid
- **Hardcoding everything:** Use variables, not just cout statements
- **Poor variable names:** Use descriptive names like `gradYear` not `x`
- **Inconsistent formatting:** Make sure your card looks professional
- **Forgetting escapes:** Remember `\"` for quotes in strings
- **No calculations:** Include at least one computed value

## Extension Challenges (Optional Bonus: +10 points)
1. **Color Challenge (+5):** Add ANSI color codes to highlight important information
2. **Interactive Version (+5):** Research how to use `cin` to let users input their own information

## Why This Matters
Creating a digital business card teaches you to:
- Organize information using appropriate data types
- Present data in a professional, readable format
- Think about user experience and visual design
- Build your professional identity as a developer

These skills directly transfer to creating user interfaces, formatting reports, and presenting data in real applications.

## Reflection Questions
Consider these as you work:
1. Why do we use different data types (string vs int vs double)?
2. How does formatting affect the professionalism of output?
3. What makes information memorable and impactful?

## Next Steps
After completing this assignment, you'll be ready for M1LAB, where you'll use variables to perform calculations and solve real business problems. Your business card shows you can present information; next, you'll manipulate and calculate with it!