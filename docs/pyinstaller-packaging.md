# Packaging the App with PyInstaller

This document describes how to create standalone executables for **Windows** and **macOS** using [PyInstaller](https://pyinstaller.org/).

## Requirements

* Python 3.9 or newer installed on the target platform.
* Install PyInstaller via pip:

```bash
pip install pyinstaller
```

## Windows

1. Open **Command Prompt** or **PowerShell**.
2. Navigate to the project directory containing your application's entry point (for example `main.py`).
3. Run PyInstaller in one-file and windowed mode:

```bash
pyinstaller --onefile --windowed main.py
```

* `--onefile` bundles everything into a single `.exe` in the `dist/` folder.
* `--windowed` prevents a console window from appearing (remove this option if the app is a command‑line tool).
4. The resulting executable will be `dist/main.exe`.

## macOS

1. Open **Terminal** and navigate to the project directory.
2. Run PyInstaller with the same options:

```bash
pyinstaller --onefile --windowed main.py
```

* The application bundle will appear under `dist/main.app`.

### Code Signing and Notarization

macOS users may encounter security warnings if the app is unsigned. To distribute widely, sign the bundle with a valid Apple Developer ID and notarize it:

```bash
codesign --deep --sign "Developer ID Application: <Your Name>" dist/main.app
xcrun altool --notarize-app --primary-bundle-id com.example.main --username <apple-id> --password <app-specific-password> --file dist/main.app
```

Follow Apple's notarization instructions if you plan to share the app outside your organization.

## Distributing the Executables

* **Windows**: Zip the `dist/main.exe` file or create an installer (e.g., using Inno Setup). Users can double-click the executable to launch the app without opening a terminal.
* **macOS**: Zip the `dist/main.app` bundle or package it into a `.dmg`. After downloading and unzipping, users can double-click the `.app` to run it.

You can share the archive through your website, email, or a file-sharing service. No additional Python installation is required on the end user's machine.
