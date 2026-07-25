# Module 2: User Input and Advanced Calculations

## Module Overview
This module transforms static programs into interactive applications. Students learn to gather user input, perform complex calculations, and present results professionally. Building directly on Module 1's foundation, programs now respond dynamically to user needs.

## Learning Path

### Week 3: Interactive Programming
- **M2T1: Interactive Farmer's Market** - Transform hardcoded values to user input
- **M2T2: Restaurant Bill Calculator** - Percentage calculations and professional formatting

### Week 4: Business Applications  
- **M2LAB1: Crate Manufacturing Analysis** - Complex business calculations and reporting
- **M2HW1: Multi-Program Challenge** - Banking, pizza party, and more with tiered grading

## Assignment Summaries

### M2T1: Interactive Farmer's Market
Students convert the Module 1 apple orchard into a dynamic marketplace system that any vendor can customize.
- **Skills:** Basic `cin`, input prompts, buffer management
- **Key Concepts:** Input validation basics, user experience design
- **Deliverable:** Fully interactive vendor setup system

### M2T2: Restaurant Bill Calculator
A smart tip calculator that handles tax, multiple tip options, and bill splitting for groups.
- **Skills:** Percentage calculations, `iomanip` formatting, complex math
- **Key Concepts:** Financial calculations, professional output formatting
- **Deliverable:** Restaurant-quality bill calculator with receipt

### M2LAB1: Crate Manufacturing Case Study
Based on Gaddis Chapter 3, students solve a real business problem involving cost analysis and profit margins.
- **Skills:** Multi-step problem solving, business logic, 3D geometry
- **Key Concepts:** Problem decomposition, pseudocode, business analysis
- **Deliverable:** Complete cost analysis system with recommendations

### M2HW1: Multi-Program Challenge
Introduces tiered grading where students choose their challenge level by selecting how many programs to complete.
- **Skills:** String manipulation, diverse problem solving, code organization
- **Programs:** Banking system, updated crates, pizza calculator, spirit generator
- **Deliverable:** 2-4 programs based on chosen tier (Bronze/Silver/Gold)

## Key Pedagogical Features

### Input Progression
1. Simple single values (`cin >>`)
2. Strings with spaces (`getline()`)
3. Mixed input types (buffer management)
4. Multiple related inputs (data collection)

### Common Input Challenges Addressed
- **The Space Problem:** Why `cin >>` stops at spaces
- **The Buffer Problem:** Leftover newlines causing issues
- **The Prompt Problem:** Importance of clear instructions
- **The Type Problem:** Handling mismatched input types

### Tiered Grading System (Introduced in M2HW1)
- **Bronze (80%):** Complete 2 programs - good for struggling students
- **Silver (90%):** Complete 3 programs - standard expectation
- **Gold (100%):** Complete all 4 programs - full mastery
- **Diamond (110%):** All programs + improvements - exceeding expectations

## Technical Skills Developed

### C++ Concepts Mastered
```cpp
// Input techniques
cin >> variable;                    // Basic input
getline(cin, stringVar);           // Full line input
cin.ignore();                       // Buffer clearing

// Output formatting
#include <iomanip>
cout << fixed << setprecision(2);  // Currency format
cout << setw(10) << right;         // Alignment

// String operations  
string full = first + " " + last;  // Concatenation

// Mathematical operations
double percent = (part / whole) * 100;
int leftover = total % portions;
```

### Professional Practices
- Clear user prompts
- Input validation concepts
- Professional receipt/report formatting
- Business logic implementation

## Assessment Strategy

### Consistent Rubric Elements
All assignments evaluate:
1. **Functionality (35-40%)** - Does it work correctly?
2. **User Experience (20-25%)** - Clear prompts and output?
3. **Code Quality (20%)** - Well-organized and commented?
4. **Formatting (15-20%)** - Professional presentation?
5. **Problem Solving (10%)** - Appropriate approach?

### Progressive Complexity
- M2T1: 25% difficulty - Basic input/output conversion
- M2T2: 35% difficulty - Calculations with formatting
- M2LAB1: 55% difficulty - Complex business logic
- M2HW1: 70% difficulty - Multiple integrated programs

## Module Resources

### Required Materials
- Module slides on input/output streams
- Gaddis Chapter 3 (especially section 3.11)
- `iomanip` reference guide

### Common Issues and Solutions

#### Issue: "Jane Smith" only stores "Jane"
**Cause:** `cin >>` stops at whitespace  
**Solution:** Use `getline(cin, name)` for full lines

#### Issue: `getline()` seems to skip input
**Cause:** Leftover newline in buffer  
**Solution:** Add `cin.ignore()` after `cin >>`

#### Issue: Money shows as 19.990000
**Cause:** Default floating-point precision  
**Solution:** Use `fixed` and `setprecision(2)`

#### Issue: Columns don't align
**Cause:** Variable-width output  
**Solution:** Use `setw()` and `left`/`right`

## Success Metrics
By completing Module 2, students can:
- ✅ Create fully interactive programs
- ✅ Handle various input scenarios gracefully
- ✅ Perform complex multi-step calculations
- ✅ Format output professionally (especially currency)
- ✅ Solve real business problems with code
- ✅ Debug common input-related issues
- ✅ Design user-friendly interfaces

## Instructor Notes

### Pacing Recommendations
- **M2T1:** 2-3 hours (includes debugging input issues)
- **M2T2:** 2-3 hours (formatting takes time)
- **M2LAB1:** 3-4 hours (complex problem)
- **M2HW1:** 3-5 hours (multiple programs)

### Differentiation Strategies
- **Struggling students:** Focus on Bronze tier in M2HW1
- **Advanced students:** Challenge with Diamond tier improvements
- **Different backgrounds:** Multiple problem domains (business, food service, education)

### Key Teaching Points
1. **Always prompt before input** - Users aren't mind readers
2. **Buffer management matters** - Explain the input stream
3. **Test with various inputs** - Edge cases reveal bugs
4. **Format money properly** - Professionalism matters

### Common Student Struggles
1. **Mixing `cin` and `getline()`** - Spend time on this
2. **Forgetting prompts** - Emphasize UX
3. **Poor formatting** - Show professional examples
4. **Integer division** - Demonstrate the problem clearly

## Looking Ahead to Module 3
Module 3 will introduce selection statements (if/else), allowing programs to make decisions. Students will enhance their Module 2 programs with:
- Input validation ("Please enter a positive number")
- Conditional responses (different messages based on values)
- Menu systems (user chooses options)
- Error handling (graceful failure)

## Module Reflection
Module 2 represents a crucial transition from "programs that run" to "programs people can use." The focus on user interaction, professional formatting, and real-world problems prepares students for actual software development. The tiered grading system introduced in M2HW1 allows students to self-differentiate while maintaining high standards.

The progression from simple input to complex business calculations with professional output demonstrates that even beginning programmers can create useful, real-world applications. By the end of Module 2, students have the skills to create interactive tools that solve genuine problems.

## Sample Success Story
"After completing Module 2, one student used their skills to create a tip calculator app for their restaurant job. Their manager was so impressed, they now use it for training new servers!" 

This is the power of practical, applicable programming education.