# Setting Up Your GitHub Codespace

Welcome to your first hands-on exercise! We'll set up your personal development environment in the cloud.

## Why Codespaces?

- ☁️ No installation needed - works on any computer
- 🔧 Pre-configured with everything you need
- 🎨 Customizable to your preferences
- 📱 Access from anywhere with internet

## Step 1: Create Your Codespace

1. Navigate to the course repository
2. Click the green "Code" button
3. Select "Codespaces" tab
4. Click "Create codespace on main"

![Codespace Creation](../resources/images/create_codespace.png)
*Note: We'll add this screenshot later*

## Step 2: Explore Your Environment

Once your Codespace loads, you'll see:
- **File Explorer** (left): Navigate project files
- **Editor** (center): Write your code
- **Terminal** (bottom): Run commands

### Quick Exploration Tasks:
1. Open the terminal (View → Terminal if not visible)
2. Type `pwd` and press Enter - this shows your current directory
3. Type `g++ --version` - this confirms C++ compiler is installed

## Step 3: Make It Yours! 🎨

This is where you personalize your workspace. Try these customizations:

### A. Change Your Theme
1. Press `Ctrl+K` then `Ctrl+T` (or `Cmd+K` then `Cmd+T` on Mac)
2. Browse themes - try "Dark+", "Light+", or something colorful!
3. Pick one that's comfortable for your eyes

### B. Adjust Font Size
1. Open Settings: `Ctrl+,` (or `Cmd+,` on Mac)
2. Search for "font size"
3. Try different sizes - what works for you?

### C. Install an Extension (Optional)
1. Click Extensions icon (or `Ctrl+Shift+X`)
2. Search for "C/C++"
3. Install the Microsoft C/C++ extension

## Step 4: Create Your First File

Let's test everything works:

1. Right-click in the File Explorer
2. Select "New File"
3. Name it `test.cpp`
4. Add this code:

```cpp
#include <iostream>
using namespace std;

int main() {
    cout << "My Codespace is ready! 🚀" << endl;
    cout << "I chose the [YOUR_THEME_NAME] theme." << endl;
    return 0;
}
```

5. Save the file (`Ctrl+S` or `Cmd+S`)

## Step 5: Compile and Run

In the terminal:

```bash
g++ test.cpp -o test
./test
```

You should see your message printed!

## 🎯 Success Criteria

You've completed this exercise when:
- ✅ Your Codespace is running
- ✅ You've customized at least one setting
- ✅ You've compiled and run a C++ program

## 💡 Reflection Questions

1. What theme did you choose and why?
2. What other customizations might help you code better?
3. How is this different from programming on your local computer?

## 🚨 Troubleshooting

**Codespace won't start?**
- Check your internet connection
- Try a different browser
- Contact instructor with error message

**Compilation errors?**
- Check for typos in your code
- Make sure you saved the file
- Verify file extension is `.cpp`

## Next Step

Ready to learn the GitHub workflow? Continue to [Your First Pull Request](02_first_pull_request.md)!