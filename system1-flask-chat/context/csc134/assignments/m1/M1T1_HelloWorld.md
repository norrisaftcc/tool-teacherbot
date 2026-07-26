# M1T1: Your First Day as a Developer

## The Scenario
Congratulations! You've just been hired as a junior developer at a software company. Your team lead has asked you to set up your development environment and create your first contribution to the team's codebase - a simple program that announces your arrival to the team. This is a tradition at your company: every new developer's first commit introduces themselves to the codebase.

## Learning Objectives
By completing this assignment, you will:
- Configure GitHub Codespaces as your cloud development environment
- Write, compile, and execute your first C++ program
- Practice professional code documentation standards
- Complete your first Git commit and push
- Establish your development workflow for the semester

## Part 1: Environment Setup (25 points)

### Step 1.1: Access GitHub Codespaces
1. Navigate to our course repository
2. Click the green "Code" button and select "Create codespace on main"
3. Wait for your Codespace to initialize (this takes 1-2 minutes)
4. Take a screenshot showing your running Codespace

### Step 1.2: Personalize Your Environment
Choose ONE of the following to make the space yours:
- Install a color theme (File → Preferences → Color Theme)
- Configure your terminal prompt
- Add a useful VS Code extension (e.g., C++ Extension Pack)

Document your choice in a comment in your code.

## Part 2: Your First Program (50 points)

### Step 2.1: Create Your Program File
Create a new file called `m1t1_lastname.cpp` (use your actual last name).

### Step 2.2: Professional Header
Every professional program starts with documentation. Add this header:

```cpp
/*
    CSC 134
    M1T1 - Your First Day
    [Your Name]
    [Date]
    
    This program introduces a new developer to the team codebase.
    Personalization: [Describe what you customized in your environment]
*/
```

### Step 2.3: The Classic Hello World - With a Twist
Write a program that outputs:
1. The classic "Hello, World!" message
2. A second line introducing yourself: "My name is [Your Name]"
3. A third line stating your goal: "I'm ready to learn C++!"

Your code structure should follow this pattern:
```cpp
#include <iostream>
using namespace std;

int main() {
    // Your code here
    
    return 0;
}
```

### Step 2.4: Compile and Run
In the terminal, compile your program:
```bash
g++ -std=c++17 -Wall -Wextra m1t1_lastname.cpp -o m1t1_lastname
```

Run it:
```bash
./m1t1_lastname
```

Debug any errors until you get clean output.

## Part 3: Professional Workflow (25 points)

### Step 3.1: Your First Commit
1. In the terminal, stage your file:
   ```bash
   git add m1t1_lastname.cpp
   ```

2. Create a meaningful commit:
   ```bash
   git commit -m "Add first developer introduction program
   
   - Implements basic Hello World functionality
   - Includes personal introduction
   - Follows team coding standards"
   ```

3. Push to GitHub:
   ```bash
   git push
   ```

### Step 3.2: Verify Your Work
1. Navigate to the repository on GitHub
2. Find your file in the file browser
3. Copy the URL to your specific file
4. Take a screenshot showing your file on GitHub

## Submission Requirements

Submit the following on Canvas:
1. **Direct link** to your file on GitHub (e.g., `https://github.com/username/repo/blob/main/m1t1_lastname.cpp`)
2. **Screenshot** of your Codespace showing successful compilation and execution
3. **Screenshot** of your file on GitHub showing your commit

## Grading Rubric (100 points)

### Environment Setup (25 points)
- **Excellent (23-25):** Codespace running, personalization completed and documented
- **Good (20-22):** Codespace running, basic setup complete
- **Satisfactory (17-19):** Codespace accessed but not fully configured
- **Needs Improvement (0-16):** Incomplete or missing setup

### Program Functionality (25 points)
- **Excellent (23-25):** All three output lines correct, compiles without warnings
- **Good (20-22):** Output correct, minor compilation warnings
- **Satisfactory (17-19):** Output mostly correct, some issues
- **Needs Improvement (0-16):** Program doesn't compile or run correctly

### Code Quality (25 points)
- **Excellent (23-25):** Professional header complete, proper formatting, clear code
- **Good (20-22):** Header present, good formatting
- **Satisfactory (17-19):** Basic header, acceptable formatting
- **Needs Improvement (0-16):** Missing header or poor formatting

### Professional Workflow (25 points)
- **Excellent (23-25):** Meaningful commit message, successful push, proper file naming
- **Good (20-22):** Basic commit and push completed
- **Satisfactory (17-19):** Work submitted but workflow incomplete
- **Needs Improvement (0-16):** Git workflow not followed

## Common Issues and Solutions

### "Permission Denied" when running program
**Solution:** Make sure you compiled first, or use `chmod +x m1t1_lastname`

### "Command not found: g++"
**Solution:** Your Codespace should have g++ installed. Try `sudo apt update && sudo apt install g++`

### Git asks for username/password
**Solution:** Codespaces should authenticate automatically. Check you're in the right repository.

## Tips for Success
- Start early! Technical issues are easier to resolve when you're not rushed
- Read error messages carefully - they usually tell you exactly what's wrong
- Your first program doesn't need to be perfect, it needs to work
- Ask for help in our discussion board if you're stuck for more than 20 minutes

## Going Further (Optional Bonus: +5 points)
Add a fourth line that displays the current date. Research how to include `<ctime>` and display today's date. Document your research process in a comment.

## Why This Matters
Every professional developer remembers their first "Hello, World!" program. It's a rite of passage that confirms your development environment works and you can create, compile, and run code. More importantly, you're establishing professional habits from day one: proper documentation, version control, and clean code. These habits will serve you throughout your career.

## Next Steps
After completing this assignment, you'll be ready for M1T2, where you'll expand your program to work with variables and create more complex output. Keep your development environment ready - we'll be using it throughout the course!