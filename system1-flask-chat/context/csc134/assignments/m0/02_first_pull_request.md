# Your First Pull Request

## 🎯 Learning Goal

Master the GitHub workflow you'll use for every assignment in this course. This is how professional developers collaborate!

## The GitHub Workflow

```
Fork → Clone → Branch → Edit → Commit → Push → Pull Request → Review → Merge
```

Don't worry if this seems like a lot - we'll go step by step!

## Step 1: Fork the Repository

1. Go to the course repository
2. Click the "Fork" button (top right)
3. This creates YOUR copy of the course materials

**Why fork?** It's like making a photocopy of a textbook - you can write in your copy without affecting the original!

## Step 2: Open in Codespace (From YOUR Fork)

1. In YOUR forked repository
2. Click "Code" → "Codespaces" → "Create codespace"
3. Wait for it to load

## Step 3: Create a Branch

A branch is like a rough draft - you can make changes without affecting the main version.

In the terminal:

```bash
git checkout -b add-my-introduction
```

This creates and switches to a new branch called "add-my-introduction"

## Step 4: Make Your Changes

1. Navigate to `0_Introduction/exercises/`
2. Create a new file called `introductions/[your-github-username].md`
3. Add your introduction:

```markdown
# Introduction: [Your Name]

## About Me
- Major: [Your major]
- Year: [Freshman/Sophomore/etc]
- Hometown: [Where you're from]

## Why I'm Taking This Course
[Write 1-2 sentences]

## Programming Experience
[None? Some? What languages?]

## Something Fun
[Share a hobby or interest!]

## My Learning Style
I learn best by: [visual aids/hands-on practice/reading/discussing/etc]
```

4. Save the file

## Step 5: Commit Your Changes

Committing is like hitting "save" on a document, but better - it records exactly what changed.

```bash
git add .
git commit -m "Add my introduction - [your name]"
```

## Step 6: Push to GitHub

This uploads your changes to GitHub:

```bash
git push origin add-my-introduction
```

## Step 7: Create the Pull Request

1. Go to YOUR fork on GitHub
2. You'll see a yellow box: "Compare & pull request"
3. Click it!
4. Fill in the PR template:

```markdown
## Summary
Adding my introduction file as part of Module 0

## Changes
- Created introductions/[username].md with my information

## Testing
- [x] File follows the template
- [x] Markdown previews correctly

## Related Issue
Relates to Module 0 setup
```

5. Click "Create pull request"

## Step 8: The Review Process

In real projects:
1. Someone reviews your code
2. They might suggest changes
3. You discuss and improve
4. Finally, it gets merged!

For this exercise, your instructor will review and merge.

## 🎉 Congratulations!

You just completed the EXACT workflow you'll use for assignments:
1. Fork the assignment repository
2. Create a branch for your solution
3. Write your code
4. Commit and push
5. Create a PR for grading

## 🤔 Reflection

- What part was confusing?
- What would you like explained differently?
- How is this different from just uploading files?

## 🚨 Common Issues

**"Permission denied" when pushing?**
- Make sure you're in YOUR fork, not the main repository
- Check that you're logged in to GitHub in your Codespace

**Can't see "Compare & pull request" button?**
- Go to the Pull Requests tab
- Click "New pull request"
- Make sure the base is the main course repo

**Merge conflicts?**
- Don't worry! Ask for help
- This happens when multiple people edit the same thing

## Next Step

Now that you know the workflow, let's write some actual C++ code! Continue to [Hello, Real World!](../examples/hello_budget.cpp)