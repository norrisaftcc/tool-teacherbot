CTS-285 · Module 0 · M0.3

## M0.3 — Working in GitHub Codespaces

A GitHub Codespace gives you a development environment in the browser. It looks and behaves much like VS Code because the browser editor is based on VS Code.

### What to keep straight

- **GitHub repository:** the durable project record.
- **Codespace:** a working development environment connected to a repository.
- **Explorer:** the files currently available in the codespace workspace.
- **Terminal:** where you run commands inside that environment.
- **Commit and push/sync:** how your saved local changes become part of the GitHub repository history.

Caution

**Saving a file is not the same as committing and syncing it to GitHub.** A change can exist in a codespace without yet being preserved in the repository history.

### Basic Codespaces workflow

1. Open the correct GitHub repository.
2. Create or resume the codespace for that repository.
3. Confirm the expected project files appear in Explorer.
4. Edit and save the file.
5. Run required commands in the terminal from the correct project folder.
6. Review changes in Source Control.
7. Commit with a short message that describes the change.
8. Sync or push the commit to GitHub.
9. Open the repository on GitHub and verify that the change is visible there.

### Ports will matter later

When a web application runs inside a codespace, Codespaces can forward the application's port so you can open the running app in a browser. You will use this later in the course when you begin working with Flask. You do not need to configure that now.

### Useful resource

GitHub's official Codespaces quickstart shows how to create a codespace, edit files, use Source Control, run an application, and open a forwarded port. [Open the GitHub Codespaces quickstart](https://docs.github.com/en/codespaces/quickstart).

Outcome

Recognize the difference between a repository and a codespace and describe the save → commit → sync/push workflow that preserves project changes.

**Next:** Module 0 Ready Check.
