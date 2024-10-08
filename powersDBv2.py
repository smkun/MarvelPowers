import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import xml.etree.ElementTree as ET
import traceback
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
import sys
import os
import re  # For filename sanitization
import json  # For saving/loading data

def resource_path(relative_path):
    """
    Get the absolute path to the resource, works for development and when bundled with PyInstaller.

    Args:
        relative_path (str): The relative path to the resource.

    Returns:
        str: The absolute path to the resource.
    """
    try:
        # When using PyInstaller, sys._MEIPASS is the temporary folder created
        base_path = sys._MEIPASS
    except AttributeError:
        # For development, use the current directory
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class PowerSelectionApp:
    def __init__(self, root):
        """
        Initialize the Power Selection App.

        Args:
            root (tk.Tk): The root Tkinter window.
        """
        self.root = root
        self.root.title("Power Selection App")
        self.root.geometry("1000x600")  # Set window size

        # Load powers from the XML file
        self.powers = self.load_powers(resource_path("powers.xml"))

        # Collect and sort power sets
        power_set_list = []
        for power in self.powers.values():
            power_set_str = power.get('PowerSet', '')
            power_set_list.extend(power_set_str.split(', '))

        # Remove duplicates and sort
        self.power_sets = sorted(set(filter(None, power_set_list)))

        # Initialize the list of selected powers
        self.selected_powers = []

        # Create the GUI widgets
        self.create_widgets()

    def load_powers(self, filename):
        """
        Load powers from an XML file.

        Args:
            filename (str): The path to the XML file.

        Returns:
            dict: A dictionary of powers.

        Raises:
            Various exceptions if the file cannot be read or parsed.
        """
        powers = {}
        try:
            tree = ET.parse(filename)
            root = tree.getroot()
            for power in root.findall('Power'):
                name = power.find('Name').text
                powers[name] = {child.tag: child.text for child in power}
        except ET.ParseError as e:
            messagebox.showerror("XML Parse Error", f"An error occurred while parsing '{filename}':\n{e}")
            self.root.destroy()
        except FileNotFoundError:
            messagebox.showerror("File Not Found", f"The file '{filename}' was not found.")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{traceback.format_exc()}")
            self.root.destroy()
        return powers

    def create_widgets(self):
        """
        Create all the GUI widgets for the application.
        """
        # Hero Name entry at the top
        hero_frame = ttk.Frame(self.root, padding="10")
        hero_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(hero_frame, text="Hero Name:").pack(side=tk.LEFT)
        self.hero_name_entry = ttk.Entry(hero_frame)
        self.hero_name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        # Add "New", "Open", and "Save" buttons
        self.new_button = ttk.Button(hero_frame, text="New", command=self.reset_app)
        self.new_button.pack(side=tk.LEFT, padx=5)
        self.open_button = ttk.Button(hero_frame, text="Open", command=self.load_from_file)
        self.open_button.pack(side=tk.LEFT, padx=5)
        self.save_button = ttk.Button(hero_frame, text="Save", command=self.save_to_file)
        self.save_button.pack(side=tk.LEFT, padx=5)

        # Left frame for power set selection and search
        left_frame = ttk.Frame(self.root, padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(left_frame, text="Power Sets:").pack(anchor=tk.W)
        self.power_set_listbox = tk.Listbox(left_frame, height=10)
        self.power_set_listbox.pack(fill=tk.X, expand=True)
        for power_set in self.power_sets:
            self.power_set_listbox.insert(tk.END, power_set)
        self.power_set_listbox.bind('<<ListboxSelect>>', self.on_power_set_select)

        ttk.Label(left_frame, text="Search by Name:").pack(anchor=tk.W, pady=(10, 0))
        self.search_entry = ttk.Entry(left_frame)
        self.search_entry.pack(fill=tk.X, expand=True)
        self.search_entry.bind('<KeyRelease>', self.on_search)

        # Middle frame for power list
        middle_frame = ttk.Frame(self.root, padding="10")
        middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(middle_frame, text="Powers:").pack(anchor=tk.W)
        self.power_listbox = tk.Listbox(middle_frame)
        self.power_listbox.pack(fill=tk.BOTH, expand=True)
        self.power_listbox.bind('<<ListboxSelect>>', self.on_power_select)

        # Bind double-click event to add power
        self.power_listbox.bind('<Double-Button-1>', self.on_power_double_click)

        # Add and Remove buttons
        button_frame = ttk.Frame(middle_frame)
        button_frame.pack(pady=(5, 0))

        self.add_button = ttk.Button(button_frame, text="Add Power", command=self.add_power)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.remove_button = ttk.Button(button_frame, text="Remove Power", command=self.remove_power)
        self.remove_button.pack(side=tk.LEFT, padx=5)

        # Right frame for power details
        right_frame = ttk.Frame(self.root, padding="10")
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(right_frame, text="Power Details:").pack(anchor=tk.W)
        self.details_text = tk.Text(right_frame, wrap=tk.WORD, width=40)
        self.details_text.pack(fill=tk.BOTH, expand=True)
        self.details_text.config(state=tk.DISABLED)

        # Selected Powers frame
        selected_frame = ttk.Frame(self.root, padding="10")
        selected_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(selected_frame, text="Selected Powers:").pack(anchor=tk.W)
        self.selected_listbox = tk.Listbox(selected_frame)
        self.selected_listbox.pack(fill=tk.BOTH, expand=True)

        # Bind double-click event to remove power
        self.selected_listbox.bind('<Double-Button-1>', self.on_selected_power_double_click)

        # Export to PDF button
        export_frame = ttk.Frame(selected_frame)
        export_frame.pack(pady=(5, 0))

        self.export_button = ttk.Button(export_frame, text="Export to PDF", command=self.export_to_pdf)
        self.export_button.pack()

    def on_power_set_select(self, event):
        """
        Event handler for selecting a power set.

        Args:
            event: The Tkinter event object.
        """
        selection = event.widget.curselection()
        if selection:
            power_set = event.widget.get(selection[0])
            self.update_power_list(power_set=power_set)
        # Note: Removed the else clause to prevent resetting the powers list

    def on_search(self, event):
        """
        Event handler for searching powers by name.

        Args:
            event: The Tkinter event object.
        """
        search_term = self.search_entry.get().lower()
        matching_powers = [name for name in self.powers.keys() if search_term in name.lower()]
        self.update_power_list(matching_powers=matching_powers)

    def update_power_list(self, power_set=None, matching_powers=None):
        """
        Update the power list based on the selected power set or search term.

        Args:
            power_set (str, optional): The selected power set.
            matching_powers (list, optional): List of powers matching the search term.
        """
        self.power_listbox.delete(0, tk.END)
        if power_set:
            # Collect power names that match the selected power set
            power_names = [
                name for name, power in self.powers.items()
                if power_set in power.get('PowerSet', '').split(', ')
            ]
            # Sort the names alphabetically
            power_names.sort()
            # Insert into the listbox
            for name in power_names:
                self.power_listbox.insert(tk.END, name)
        elif matching_powers is not None:
            # Sort the matching powers alphabetically
            matching_powers.sort()
            for name in matching_powers:
                self.power_listbox.insert(tk.END, name)
        else:
            # Show all powers sorted alphabetically
            all_power_names = sorted(self.powers.keys())
            for name in all_power_names:
                self.power_listbox.insert(tk.END, name)

    def on_power_select(self, event):
        """
        Event handler for selecting a power to view its details.

        Args:
            event: The Tkinter event object.
        """
        selection = event.widget.curselection()
        if selection:
            power_name = event.widget.get(selection[0])
            self.display_power_details(power_name)

    def display_power_details(self, power_name):
        """
        Display the details of the selected power.

        Args:
            power_name (str): The name of the power.
        """
        power = self.powers.get(power_name, {})
        details = f"Name: {power.get('Name', 'N/A')}\n\n"
        details += f"Description: {power.get('Description', 'N/A')}\n\n"
        details += f"Power Set: {power.get('PowerSet', 'N/A')}\n\n"
        details += f"Prerequisites: {power.get('Prerequisites', 'N/A')}\n\n"
        details += f"Action: {power.get('Action', 'N/A')}\n\n"
        details += f"Duration: {power.get('Duration', 'N/A')}\n\n"
        details += f"Cost: {power.get('Cost', 'N/A')}\n\n"
        details += f"Effect: {power.get('Effect', 'N/A')}"

        # Update the details text widget
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(tk.END, details)
        self.details_text.config(state=tk.DISABLED)

    def add_power(self):
        """
        Add the selected power to the hero's list of selected powers.
        """
        selection = self.power_listbox.curselection()
        if selection:
            power_name = self.power_listbox.get(selection[0])
            if power_name not in self.selected_powers:
                self.selected_powers.append(power_name)
                self.selected_listbox.insert(tk.END, power_name)
            else:
                messagebox.showinfo("Information", f"'{power_name}' is already in your list.")

    def remove_power(self):
        """
        Remove the selected power from the hero's list of selected powers.
        """
        selection = self.selected_listbox.curselection()
        if selection:
            power_name = self.selected_listbox.get(selection[0])
            self.selected_powers.remove(power_name)
            self.selected_listbox.delete(selection[0])

    def on_power_double_click(self, event):
        """
        Handle double-click event on the power listbox to add a power.

        Args:
            event: The Tkinter event object.
        """
        self.add_power()

    def on_selected_power_double_click(self, event):
        """
        Handle double-click event on the selected powers listbox to remove a power.

        Args:
            event: The Tkinter event object.
        """
        self.remove_power()

    def export_to_pdf(self):
        """
        Export the selected powers to a PDF file.
        """
        if not self.selected_powers:
            messagebox.showinfo("Information", "Your selected powers list is empty.")
            return

        # Get the hero's name from the entry widget
        hero_name = self.hero_name_entry.get().strip()

        # Generate default filename
        if hero_name:
            default_filename = f"{hero_name}_powers.pdf"
        else:
            default_filename = "selected_powers.pdf"

        # Remove invalid characters from filename
        default_filename = re.sub(r'[\\/*?:"<>|]', "", default_filename)

        # Prompt user for file name and location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=default_filename,
            title="Save PDF as"
        )
        if not file_path:
            return  # User cancelled the save dialog

        # Create PDF
        try:
            c = canvas.Canvas(file_path, pagesize=letter)
            width, height = letter
            textobject = c.beginText()
            textobject.setTextOrigin(50, height - 50)
            font_name = "Helvetica"
            font_size = 12
            textobject.setFont(font_name, font_size)
            textobject.setLeading(font_size)  # Set leading to reduce line spacing
            max_line_width = width - 100  # Adjust as needed for margins

            # Add Hero Name to PDF in black
            if hero_name:
                textobject.setFillColor(colors.black)  # Ensure header is black
                header = f"Powers Selected by {hero_name}"
                wrapped_header = self.wrap_text(header, font_name, font_size, max_line_width)
                for line in wrapped_header:
                    textobject.textLine(line)
                textobject.textLine("")  # Add an empty line after the header

            for power_name in self.selected_powers:
                power = self.powers.get(power_name, {})

                # Set the color to red for the power name
                textobject.setFillColor(colors.red)
                details = f"Name: {power.get('Name', 'N/A')}"
                wrapped_lines = self.wrap_text(details, font_name, font_size, max_line_width)
                for wrapped_line in wrapped_lines:
                    textobject.textLine(wrapped_line)

                # Reset the color to black for the rest of the power details
                textobject.setFillColor(colors.black)
                details = f"Description: {power.get('Description', 'N/A')}"
                details += f"\nPower Set: {power.get('PowerSet', 'N/A')}"
                details += f"\nPrerequisites: {power.get('Prerequisites', 'N/A')}"
                details += f"\nAction: {power.get('Action', 'N/A')}"
                details += f"\nDuration: {power.get('Duration', 'N/A')}"
                details += f"\nCost: {power.get('Cost', 'N/A')}"
                details += f"\nEffect: {power.get('Effect', 'N/A')}"
                details += f"\n{'-' * 80}"

                # Wrap and render each line of the rest of the details
                for line in details.strip().split('\n'):
                    line = line.strip()
                    if not line:
                        continue  # Skip empty lines
                    wrapped_lines = self.wrap_text(line, font_name, font_size, max_line_width)
                    for wrapped_line in wrapped_lines:
                        textobject.textLine(wrapped_line)
                        # Move to next page if needed
                        if textobject.getY() < 50:
                            c.drawText(textobject)
                            c.showPage()
                            textobject = c.beginText()
                            textobject.setTextOrigin(50, height - 50)
                            textobject.setFont(font_name, font_size)
                            textobject.setLeading(font_size)
                            textobject.setFillColor(colors.black)  # Reset color after page change

                textobject.textLine("")  # Add an empty line between powers

            c.drawText(textobject)
            c.save()
            messagebox.showinfo("Success", f"Selected powers exported to '{os.path.abspath(file_path)}'.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating the PDF:\n{e}")

    def wrap_text(self, text, font_name, font_size, max_width):
        """
        Wrap text to fit within a specified width.

        Args:
            text (str): The text to wrap.
            font_name (str): The font name.
            font_size (int): The font size.
            max_width (int): The maximum width in points.

        Returns:
            list: A list of wrapped text lines.
        """
        lines = []
        words = text.split()
        current_line = ''
        for word in words:
            if current_line:
                test_line = current_line + ' ' + word
            else:
                test_line = word
            test_line_width = pdfmetrics.stringWidth(test_line, font_name, font_size)
            if test_line_width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines

    def reset_app(self):
        """
        Reset the application to its initial state.
        """
        # Clear hero name entry
        self.hero_name_entry.delete(0, tk.END)
        # Clear selected powers list
        self.selected_powers = []
        self.selected_listbox.delete(0, tk.END)
        # Reset power set selection
        self.power_set_listbox.selection_clear(0, tk.END)
        # Clear the power listbox
        self.update_power_list()
        # Clear search entry
        self.search_entry.delete(0, tk.END)
        # Clear power details
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        self.details_text.config(state=tk.DISABLED)
        # Optionally, reset any other state variables or GUI elements as needed

    def save_to_file(self):
        """
        Save the hero's name and selected powers to a JSON file.
        """
        # Get the hero's name
        hero_name = self.hero_name_entry.get().strip()

        if not hero_name:
            messagebox.showinfo("Information", "Please enter a Hero Name before saving.")
            return

        # Prepare data to save
        data = {
            'hero_name': hero_name,
            'selected_powers': self.selected_powers
        }

        # Prompt user to choose a file location
        default_filename = f"{hero_name}_powers.json"
        default_filename = re.sub(r'[\\/*?:"<>|]', "", default_filename)

        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile=default_filename,
            title="Save File As"
        )

        if not file_path:
            return  # User cancelled the save dialog

        # Save data to the file
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            messagebox.showinfo("Success", f"Data saved to '{os.path.abspath(file_path)}'.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the file:\n{e}")

    def load_from_file(self):
        """
        Load the hero's name and selected powers from a JSON file.
        """
        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Open File"
        )

        if not file_path:
            return  # User cancelled the open dialog

        # Load data from the file
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            # Update hero name
            hero_name = data.get('hero_name', '')
            self.hero_name_entry.delete(0, tk.END)
            self.hero_name_entry.insert(0, hero_name)

            # Update selected powers
            self.selected_powers = data.get('selected_powers', [])
            self.selected_listbox.delete(0, tk.END)
            for power_name in self.selected_powers:
                self.selected_listbox.insert(tk.END, power_name)

            messagebox.showinfo("Success", f"Data loaded from '{os.path.abspath(file_path)}'.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading the file:\n{e}")

if __name__ == "__main__":
    # Create the main application window
    root = tk.Tk()  # Ensure this is the first Tkinter command
    app = PowerSelectionApp(root)
    root.mainloop()
