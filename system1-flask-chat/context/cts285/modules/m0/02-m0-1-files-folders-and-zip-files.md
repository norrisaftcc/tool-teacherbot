CTS-285 · Module 0 · M0.1

## M0.1 — Files, Folders, and ZIP Files

Most avoidable development problems begin with a simple question: **Where is the file?** Before you work with code, make sure you can recognize a file, its folder, its extension, and the package it came from.

### Know what you are looking at

Example | What it tells you

`requirements.md` | A Markdown file named requirements.

`app.py` | A Python source file.

`templates/` | A folder. It can contain files and other folders.

`starter-files.zip` | A compressed package. The files inside usually must be extracted before you work with them.

### Folder habits that prevent mistakes

- Keep course work inside a clearly named CTS-285 project folder or repository.
- Do not scatter related files across Downloads, Desktop, and multiple duplicate folders.
- Read the full file name, including the extension.
- Do not rename a file extension just to make an application open it.
- Before running a command, verify which folder you are working in.

Caution

**A ZIP file is not the same thing as the folder inside it.** If instructions say to work in the extracted folder, opening files directly from the ZIP can cause missing-file, path, save, or permission problems.

### Zip and unzip

**To unzip:** locate the `.zip` file, use your operating system's Extract/Uncompress option, then open the newly created folder. Confirm that the expected files are inside before deleting the ZIP.

**To create a ZIP:** select the folder or files that belong together, use Compress/Send to ZIP, then open the resulting archive once to verify that it contains what you intended.

### Read a path from left to right

`cts-285/docs/requirements.md`

Repository or project folder → `docs` folder → `requirements.md` file.

### Quick check

****You downloaded project-files.zip. What should you do before editing?****

Extract the ZIP, open the extracted folder, and confirm that the expected files are present.

****What does the path docs/requirements.md tell you?****

The file `requirements.md` is inside a folder named `docs`.

**Next:** M0.2 — VS Code as a Text Editor.
