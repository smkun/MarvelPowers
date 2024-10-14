# MMRPG-PowersAndTraits App

![MMRPG-PowersAndTraits App Logo](MMRPG.png "MMRPG-PowersAndTraits App Logo")

## Overview

The MMRPG-PowersAndTraits App is a comprehensive tool designed for players of the Marvel Multiverse Role-Playing Game (MMRPG). It allows you to browse, select, and manage both powers and traits for your heroes. With features like power set filtering, search functionality, and detailed descriptions for both powers and traits, creating and customizing your hero has never been easier.

## Features

- **Hero Management**: Enter your hero's name and save or load your hero's power and trait selections.
- **Power and Trait Browsing**: Browse powers by power sets or search for specific powers by name. Browse all available traits.
- **Detailed Descriptions**: View comprehensive details of each power and trait, including descriptions, prerequisites, action types, durations, costs, and effects.
- **Selection Management**: Add or remove powers and traits from your hero's selection list with simple clicks or double-clicks.
- **Export to PDF**: Export your selected powers and traits to a neatly formatted PDF for easy reference.
- **Save/Load Functionality**: Save your hero's details (including name, powers, and traits) to a JSON file and load them later.
- **User-Friendly Interface**: Intuitive design for easy navigation and power/trait management.

## Installation

### Windows Users

1. **Locate the Executable**:
   - The Windows executable file (`MMRPG-PowersAndTraits.exe`) is located in the `dist` folder after building with PyInstaller.
2. **Run the Application**:
   - Double-click on `MMRPG-PowersAndTraits.exe` to launch the app.

### macOS Users

1. **Locate the Application**:
   - The macOS application (`MMRPG-PowersAndTraits.app`) is located in the `dist` folder after building with PyInstaller.
2. **Run the Application**:
   - Double-click on `MMRPG-PowersAndTraits.app` to launch the app.
   - **Note**: You may need to adjust your security settings to allow the app to run.

### Running from Source Code

If you prefer to run the application from the source code:

1. **Prerequisites**:
   - Python 3.x installed on your system.
   - Required Python packages:
     - `tkinter` (usually comes pre-installed with Python)
     - `reportlab`

2. **Install Required Packages**:
   ```bash
   pip install reportlab
   ```

3. **Run the Application**:
   - Navigate to the directory containing `MMRPG-PowersAndTraits.py`.
   - Execute the script:
     ```bash
     python MMRPG-PowersAndTraits.py
     ```

## Usage Instructions

1. **Launch the Application**:
   - Use the executable or run the script as described above.

2. **Create a New Hero**:
   - Enter your hero's name in the "Hero Name" field at the top.

3. **Browse Powers**:
   - **By Power Set**:
     - Select a power set from the "Power Sets" list to filter powers.
   - **By Name**:
     - Use the "Search Powers by Name" field to find powers containing specific keywords.

4. **Browse Traits**:
   - All available traits are listed in the traits listbox.

5. **View Details**:
   - Click on a power or trait to display its details on the right side.

6. **Select Powers and Traits**:
   - **Add Power/Trait**:
     - Double-click on a power or trait, or select it and click the respective "Add" button.
   - **Remove Power/Trait**:
     - Double-click on a selected power or trait in the "Selected Powers" or "Selected Traits" list to remove it.

7. **Manage Hero Data**:
   - **New**:
     - Click "New" to reset the app and create a new hero.
   - **Save**:
     - Click "Save" to save your hero's name, selected powers, and traits to a JSON file.
   - **Open**:
     - Click "Open" to load a saved hero from a JSON file.

8. **Export to PDF**:
   - Click "Export to PDF" to save your selected powers and traits to a PDF file. The PDF will include all the details of the selected powers and traits for easy reference.

## Building the Application

To build the standalone application:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Run PyInstaller with the provided spec file:
   ```bash
   pyinstaller MMRPG-PowersAndTraits.spec
   ```

3. The built application will be in the `dist` folder.

## Files and Folders

- **`MMRPG-PowersAndTraits.py`**: The main Python script for the application.
- **`powers.xml`**: XML file containing all the power data used by the application.
- **`traits.xml`**: XML file containing all the trait data used by the application.
- **`MMRPG-PowersAndTraits.spec`**: PyInstaller spec file for building the standalone application.
- **`MMRPG.ico`**: Icon file for the Windows executable.

## Notes

- The application uses `powers.xml` and `traits.xml` as the data sources. Ensure these files are present in the same directory as the executable or script.
- When exporting to PDF or saving/loading heroes, the application will prompt you to choose a file location.

## Troubleshooting

- **Application Doesn't Start**:
  - Ensure that all required files (`powers.xml`, `traits.xml`, etc.) are in the correct directories.
  - For macOS, you may need to adjust your security settings to allow apps from unidentified developers.

- **Dependencies Issues**:
  - If running from source and encountering errors, make sure all required Python packages are installed.

- **PDF Export Fails**:
  - Check that you have write permissions to the destination folder.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests on the GitHub repository.

## License

This project is licensed under the MIT License.

## Contact

For support or inquiries, please contact:

- **Name**: [Scott Kunian]
- **Email**: [scott@scottkunian.com]

---

Thank you for using the MMRPG-PowersAndTraits App! We hope it enhances your MMRPG experience.