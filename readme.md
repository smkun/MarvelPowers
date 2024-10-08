# Marvel Powers Selection App

## Overview

The Marvel Powers Selection App is a tool designed for players of the Marvel Multiverse Role-Playing Game (MMRPG). It allows you to browse, select, and manage powers for your heroes. With features like power set filtering, search functionality, and detailed power descriptions, creating and customizing your hero has never been easier.

## Features

- **Hero Management**: Enter your hero's name and save or load your hero's power selections.
- **Power Browsing**: Browse powers by power sets or search for specific powers by name.
- **Detailed Descriptions**: View comprehensive details of each power, including description, prerequisites, action type, duration, cost, and effect.
- **Selection Management**: Add or remove powers from your hero's selection list with simple clicks.
- **Export to PDF**: Export your selected powers to a neatly formatted PDF for easy reference.
- **User-Friendly Interface**: Intuitive design for easy navigation and power management.

## Installation

### Windows Users

1. **Locate the Executable**:
   - The Windows executable file (`MarvelPowers.exe`) is located in the `MMRPG-PC` folder.
2. **Run the Application**:
   - Double-click on `MarvelPowers.exe` to launch the app.

### macOS Users

1. **Locate the Application**:
   - The macOS application (`MarvelPowers.app`) is located in the `MMRPG-OS` folder.
2. **Run the Application**:
   - Double-click on `MarvelPowers.app` to launch the app.
   - **Note**: You may need to adjust your security settings to allow the app to run.

### Running from Source Code

If you prefer to run the application from the source code:

1. **Prerequisites**:
   - Python 3.x installed on your system.
   - Required Python packages:
     - `tkinter`
     - `reportlab`

2. **Install Required Packages**:
   ```bash
   pip install reportlab
   ```
   - Note: `tkinter` usually comes pre-installed with Python on Windows and macOS.

3. **Run the Application**:
   - Navigate to the directory containing `powersDBv2.py`.
   - Execute the script:
     ```bash
     python powersDBv2.py
     ```

## Usage Instructions

1. **Launch the Application**:
   - Use the executable in `MMRPG-PC` or `MMRPG-OS` folders, or run the script as described above.

2. **Create a New Hero**:
   - Enter your hero's name in the "Hero Name" field at the top.

3. **Browse Powers**:
   - **By Power Set**:
     - Select a power set from the "Power Sets" list to filter powers.
   - **By Name**:
     - Use the "Search by Name" field to find powers containing specific keywords.

4. **View Power Details**:
   - Click on a power in the "Powers" list to display its details on the right side.

5. **Select Powers**:
   - **Add Power**:
     - Double-click on a power or select it and click the "Add Power" button to add it to your hero's selection.
   - **Remove Power**:
     - Double-click on a selected power in the "Selected Powers" list or select it and click the "Remove Power" button to remove it.

6. **Manage Hero Data**:
   - **New**:
     - Click "New" to reset the app and create a new hero.
   - **Save**:
     - Click "Save" to save your hero's name and selected powers to a `.json` file.
   - **Open**:
     - Click "Open" to load a saved hero from a `.json` file.

7. **Export to PDF**:
   - Click "Export to PDF" to save your selected powers to a PDF file. The PDF will include all the details of the selected powers for easy reference.

## Files and Folders

- **`MMRPG-PC` Folder**:
  - Contains the Windows executable (`MarvelPowers.exe`) for easy access on Windows systems.

- **`MMRPG-OS` Folder**:
  - Contains the macOS application (`MarvelPowers.app`) for easy access on macOS systems.

- **`powersDBv2.py`**:
  - The main Python script for the application if running from source code.

- **`powers.xml`**:
  - An XML file containing all the power data used by the application. This file is required and should be in the same directory as the executable or script.

## Notes

- The application uses `powers.xml` as the data source for all powers. Ensure this file is present in the same directory as the executable or script.
- When exporting to PDF or saving/loading heroes, the application will prompt you to choose a file location.

## Troubleshooting

- **Application Doesn't Start**:
  - Ensure that all required files (`powers.xml`, etc.) are in the correct directories.
  - For macOS, you may need to adjust your security settings to allow apps from unidentified developers.

- **Dependencies Issues**:
  - If running from source and encountering errors, make sure all required Python packages are installed.

- **PDF Export Fails**:
  - Check that you have write permissions to the destination folder.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests on the [GitHub repository](#).

## License

This project is licensed under the MIT License.

## Contact

For support or inquiries, please contact:

- **Name**: [Scott Kunian]
- **Email**: [skunian@yahoo.com]

---

Thank you for using the Marvel Powers Selection App! We hope it enhances your MMRPG experience.