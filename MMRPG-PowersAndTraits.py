import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import xml.etree.ElementTree as ET
import traceback
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import sys
import os
import re  # For filename sanitization
import json  # For saving/loading data
from reportlab.pdfbase import pdfmetrics

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

class PowerAndTraitSelectionApp:
    def __init__(self, root):
        """
        Initialize the Power and Trait Selection App.

        Args:
            root (tk.Tk): The root Tkinter window.
        """
        self.root = root
        self.root.title("MMRPG-PowersAndTraits App")
        self.root.geometry("1200x700")  # Set window size

        # Load powers and traits from the XML files
        self.powers = self.load_powers(resource_path("powers.xml"))
        self.traits = self.load_traits(resource_path("traits.xml"))

        # Collect and sort power sets
        power_set_list = []
        for power in self.powers.values():
            power_set_str = power.get('PowerSet', '')
            power_set_list.extend(power_set_str.split(', '))

        # Remove duplicates and sort
        self.power_sets = sorted(set(filter(None, power_set_list)))

        # Initialize the list of selected powers and traits
        self.selected_powers = []
        self.selected_traits = []

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

    def load_traits(self, filename):
        """
        Load traits from an XML file.

        Args:
            filename (str): The path to the XML file.

        Returns:
            dict: A dictionary of traits.

        Raises:
            Various exceptions if the file cannot be read or parsed.
        """
        traits = {}
        try:
            tree = ET.parse(filename)
            root = tree.getroot()
            for trait in root.findall('trait'):
                name = trait.find('name').text
                traits[name] = {child.tag: child.text for child in trait}
        except ET.ParseError as e:
            messagebox.showerror("XML Parse Error", f"An error occurred while parsing '{filename}':\n{e}")
            self.root.destroy()
        except FileNotFoundError:
            messagebox.showerror("File Not Found", f"The file '{filename}' was not found.")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{traceback.format_exc()}")
            self.root.destroy()
        return traits

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

        ttk.Label(left_frame, text="Search Powers by Name:").pack(anchor=tk.W, pady=(10, 0))
        self.search_entry = ttk.Entry(left_frame)
        self.search_entry.pack(fill=tk.X, expand=True)
        self.search_entry.bind('<KeyRelease>', self.on_search_powers)

        # Middle frame for power list and trait list
        middle_frame = ttk.Frame(self.root, padding="10")
        middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(middle_frame, text="Powers:").pack(anchor=tk.W)
        self.power_listbox = tk.Listbox(middle_frame)
        self.power_listbox.pack(fill=tk.BOTH, expand=True)
        self.power_listbox.bind('<<ListboxSelect>>', self.on_power_select)
        self.power_listbox.bind('<Double-Button-1>', self.on_power_double_click)

        ttk.Label(middle_frame, text="Traits:").pack(anchor=tk.W, pady=(10, 0))
        self.trait_listbox = tk.Listbox(middle_frame)
        self.trait_listbox.pack(fill=tk.BOTH, expand=True)
        for trait in self.traits.keys():
            self.trait_listbox.insert(tk.END, trait)
        self.trait_listbox.bind('<<ListboxSelect>>', self.on_trait_select)
        self.trait_listbox.bind('<Double-Button-1>', self.on_trait_double_click)

        # Right frame for power and trait details
        right_frame = ttk.Frame(self.root, padding="10")
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(right_frame, text="Details:").pack(anchor=tk.W)
        self.details_text = tk.Text(right_frame, wrap=tk.WORD, width=40)
        self.details_text.pack(fill=tk.BOTH, expand=True)
        self.details_text.config(state=tk.DISABLED)

        # Selected Powers and Traits frame
        selected_frame = ttk.Frame(self.root, padding="10")
        selected_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(selected_frame, text="Selected Powers:").pack(anchor=tk.W)
        self.selected_power_listbox = tk.Listbox(selected_frame)
        self.selected_power_listbox.pack(fill=tk.BOTH, expand=True)
        self.selected_power_listbox.bind('<Double-Button-1>', self.on_selected_power_double_click)

        ttk.Label(selected_frame, text="Selected Traits:").pack(anchor=tk.W, pady=(10, 0))
        self.selected_trait_listbox = tk.Listbox(selected_frame)
        self.selected_trait_listbox.pack(fill=tk.BOTH, expand=True)
        self.selected_trait_listbox.bind('<Double-Button-1>', self.on_selected_trait_double_click)

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

    def on_search_powers(self, event):
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
        Update the list of powers displayed in the power listbox based on the selected power set or search term.

        Args:
            power_set (str, optional): The selected power set to filter powers by.
            matching_powers (list, optional): A list of power names matching the search term.
        """
        self.power_listbox.delete(0, tk.END)

        if matching_powers is not None:
            for power_name in matching_powers:
                self.power_listbox.insert(tk.END, power_name)
        elif power_set is not None:
            for power_name, power_data in self.powers.items():
                if power_set in power_data.get('PowerSet', ''):
                    self.power_listbox.insert(tk.END, power_name)

    def on_power_select(self, event):
        """
        Event handler for selecting a power to view its details.

        Args:
            event: The Tkinter event object.
        """
        selection = event.widget.curselection()
        if selection:
            power_name = event.widget.get(selection[0])
            self.display_details(self.powers.get(power_name, {}))

    def on_trait_select(self, event):
        """
        Event handler for selecting a trait to view its details.

        Args:
            event: The Tkinter event object.
        """
        selection = event.widget.curselection()
        if selection:
            trait_name = event.widget.get(selection[0])
            self.display_details(self.traits.get(trait_name, {}))

    def display_details(self, data):
        """
        Display the details of the selected power or trait.

        Args:
            data (dict): The data of the power or trait.
        """
        details = "\n".join([f"{key}: {value}" for key, value in data.items()])

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
                self.selected_power_listbox.insert(tk.END, power_name)
            else:
                messagebox.showinfo("Information", f"'{power_name}' is already in your list.")

    def add_trait(self):
        """
        Add the selected trait to the hero's list of selected traits.
        """
        selection = self.trait_listbox.curselection()
        if selection:
            trait_name = self.trait_listbox.get(selection[0])
            if trait_name not in self.selected_traits:
                self.selected_traits.append(trait_name)
                self.selected_trait_listbox.insert(tk.END, trait_name)
            else:
                messagebox.showinfo("Information", f"'{trait_name}' is already in your list.")

    def on_power_double_click(self, event):
        """
        Handle double-click event on the power listbox to add a power.

        Args:
            event: The Tkinter event object.
        """
        self.add_power()

    def on_trait_double_click(self, event):
        """
        Handle double-click event on the trait listbox to add a trait.

        Args:
            event: The Tkinter event object.
        """
        self.add_trait()

    def on_selected_power_double_click(self, event):
        """
        Handle double-click event on the selected powers listbox to remove a power.

        Args:
            event: The Tkinter event object.
        """
        selection = self.selected_power_listbox.curselection()
        if selection:
            power_name = self.selected_power_listbox.get(selection[0])
            self.selected_powers.remove(power_name)
            self.selected_power_listbox.delete(selection[0])

    def on_selected_trait_double_click(self, event):
        """
        Handle double-click event on the selected traits listbox to remove a trait.

        Args:
            event: The Tkinter event object.
        """
        selection = self.selected_trait_listbox.curselection()
        if selection:
            trait_name = self.selected_trait_listbox.get(selection[0])
            self.selected_traits.remove(trait_name)
            self.selected_trait_listbox.delete(selection[0])

    def export_to_pdf(self):
        """
        Export the selected powers and traits to a PDF file, including all their details.
        """
        if not self.selected_powers and not self.selected_traits:
            messagebox.showinfo("Information", "Your selected powers and traits list is empty.")
            return

        # Get the hero's name from the entry widget
        hero_name = self.hero_name_entry.get().strip()

        # Generate default filename
        if hero_name:
            default_filename = f"{hero_name}_powers_and_traits.pdf"
        else:
            default_filename = "selected_powers_and_traits.pdf"

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
            x_margin = 50
            y_margin = 50
            font_name = "Helvetica"
            font_size = 9  # Reduced font size to 9pt

            # Calculate column widths and positions
            column_gap = 20  # Gap between columns
            num_columns = 2
            column_width = (width - 2 * x_margin - column_gap) / num_columns
            max_line_width = column_width  # Adjust max line width for columns

            # Starting positions for columns
            column_x_positions = [x_margin, x_margin + column_width + column_gap]
            current_column = 0  # Start with the first column

            textobject = c.beginText()
            textobject.setTextOrigin(column_x_positions[current_column], height - y_margin)
            textobject.setFont(font_name, font_size)
            textobject.setLeading(font_size * 1.2)  # Set leading to adjust line spacing

            # Function to handle column and page breaks
            def check_space(lines_needed):
                nonlocal textobject, current_column
                if textobject.getY() - lines_needed * font_size * 1.2 < y_margin:
                    if current_column < num_columns - 1:
                        # Move to next column
                        current_column += 1
                        textobject.setTextOrigin(column_x_positions[current_column], height - y_margin)
                    else:
                        # Start a new page
                        c.drawText(textobject)
                        c.showPage()
                        # Reset text object and column
                        textobject = c.beginText()
                        current_column = 0
                        textobject.setTextOrigin(column_x_positions[current_column], height - y_margin)
                        textobject.setFont(font_name, font_size)
                        textobject.setLeading(font_size * 1.2)

            # Function to calculate the number of lines required for a block of text
            def calculate_lines(wrapped_texts):
                return sum(len(wrapped_text) for wrapped_text in wrapped_texts)

            # Add Hero Name to PDF in black
            if hero_name:
                textobject.setFillColor(colors.black)  # Ensure header is black
                header_font_size = font_size + 2
                textobject.setFont('Helvetica-Bold', header_font_size)  # Slightly larger font for header
                wrapped_header = self.wrap_text(f"{hero_name}'s Powers and Traits", 'Helvetica-Bold',
                                                header_font_size, max_line_width)
                check_space(len(wrapped_header) + 1)
                for line in wrapped_header:
                    textobject.textLine(line)
                textobject.textLine("")  # Add an empty line after the header
                textobject.setFont(font_name, font_size)  # Reset font

            # Add selected powers to PDF
            if self.selected_powers:
                # Section title
                textobject.setFillColor(colors.black)
                title_font_size = font_size + 1
                textobject.setFont('Helvetica-Bold', title_font_size)
                wrapped_title = self.wrap_text("Selected Powers:", 'Helvetica-Bold', title_font_size, max_line_width)
                check_space(len(wrapped_title) + 1)
                for line in wrapped_title:
                    textobject.textLine(line)
                textobject.textLine("")
                textobject.setFont(font_name, font_size)  # Reset font

                for power_name in self.selected_powers:
                    power_data = self.powers.get(power_name, {})
                    # Collect all required fields
                    fields = {
                        'Name': power_data.get('Name', power_name),
                        'Description': power_data.get('Description', 'No description provided.'),
                        'PowerSet': power_data.get('PowerSet', 'N/A'),
                        'Prerequisites': power_data.get('Prerequisites', 'None'),
                        'Action': power_data.get('Action', 'N/A'),
                        'Trigger': power_data.get('Trigger', 'N/A'),
                        'Duration': power_data.get('Duration', 'N/A'),
                        'Range': power_data.get('Range', 'N/A'),
                        'Cost': power_data.get('Cost', 'N/A'),
                        'Effect': power_data.get('Effect', 'N/A')
                    }
                    # Prepare the texts to be written
                    # Power Name
                    text_lines = []
                    power_name_wrapped = self.wrap_text(fields['Name'], 'Helvetica-Bold', font_size, max_line_width)
                    text_lines.append(power_name_wrapped)
                    # Other fields
                    for key in ['Description', 'PowerSet', 'Prerequisites', 'Action', 'Trigger', 'Duration', 'Range', 'Cost', 'Effect']:
                        value = fields.get(key)
                        if value and value not in ['N/A', 'None', 'No description provided.']:
                            field_text = f"{key}: {value}"
                            wrapped_field = self.wrap_text(field_text, font_name, font_size, max_line_width)
                            text_lines.append(wrapped_field)
                    text_lines.append([''])  # Add an empty line after each power

                    # Calculate total lines needed for this power
                    total_lines_needed = calculate_lines(text_lines)
                    check_space(total_lines_needed)

                    # Write the power's details
                    # Power name in red and bold
                    textobject.setFillColor(colors.red)  # Power names in red
                    textobject.setFont('Helvetica-Bold', font_size)
                    for line in power_name_wrapped:
                        textobject.textLine(line)
                    # Reset to black and regular font
                    textobject.setFillColor(colors.black)
                    textobject.setFont(font_name, font_size)
                    # Write other fields
                    for wrapped_field in text_lines[1:-1]:  # Skip the first (power name) and last (empty line)
                        for line in wrapped_field:
                            textobject.textLine(line)
                    textobject.textLine('')  # Empty line after the power

            # Add selected traits to PDF
            if self.selected_traits:
                # Section title
                textobject.setFillColor(colors.black)
                title_font_size = font_size + 1
                textobject.setFont('Helvetica-Bold', title_font_size)
                wrapped_title = self.wrap_text("Selected Traits:", 'Helvetica-Bold', title_font_size, max_line_width)
                check_space(len(wrapped_title) + 1)
                for line in wrapped_title:
                    textobject.textLine(line)
                textobject.textLine("")
                textobject.setFont(font_name, font_size)  # Reset font

                for trait_name in self.selected_traits:
                    trait_data = self.traits.get(trait_name, {})
                    # Collect required fields
                    fields = {
                        'Name': trait_data.get('name', trait_name),
                        'Description': trait_data.get('description', 'No description provided.')
                    }
                    # Prepare the texts to be written
                    # Trait Name
                    text_lines = []
                    trait_name_wrapped = self.wrap_text(fields['Name'], 'Helvetica-Bold', font_size, max_line_width)
                    text_lines.append(trait_name_wrapped)
                    # Description
                    if fields['Description'] and fields['Description'] != 'No description provided.':
                        description_wrapped = self.wrap_text(f"Description: {fields['Description']}", font_name,
                                                             font_size, max_line_width)
                        text_lines.append(description_wrapped)
                    text_lines.append([''])  # Add an empty line after each trait

                    # Calculate total lines needed for this trait
                    total_lines_needed = calculate_lines(text_lines)
                    check_space(total_lines_needed)

                    # Write the trait's details
                    # Trait name in blue and bold
                    textobject.setFillColor(colors.blue)  # Trait names in blue
                    textobject.setFont('Helvetica-Bold', font_size)
                    for line in trait_name_wrapped:
                        textobject.textLine(line)
                    # Reset to black and regular font
                    textobject.setFillColor(colors.black)
                    textobject.setFont(font_name, font_size)
                    # Write description
                    if fields['Description'] and fields['Description'] != 'No description provided.':
                        for line in description_wrapped:
                            textobject.textLine(line)
                    textobject.textLine('')  # Empty line after the trait

            # Draw any remaining text
            c.drawText(textobject)
            c.save()
            messagebox.showinfo("Success", f"Powers and traits successfully exported to '{file_path}'.")
        except Exception as e:
            messagebox.showerror("Error",
                                 f"An unexpected error occurred while exporting to PDF:\n{traceback.format_exc()}")

    def wrap_text(self, text, font_name, font_size, max_width):
        """
        Wrap text to fit within a specified width.

        Args:
            text (str): The text to wrap.
            font_name (str): The name of the font.
            font_size (int): The size of the font.
            max_width (float): The maximum width in points.

        Returns:
            list: A list of wrapped lines.
        """
        wrapped_lines = []
        words = text.split()
        line = ""
        for word in words:
            test_line = f"{line} {word}".strip()
            if pdfmetrics.stringWidth(test_line, font_name, font_size) <= max_width:
                line = test_line
            else:
                wrapped_lines.append(line)
                line = word
        if line:
            wrapped_lines.append(line)
        return wrapped_lines

    def reset_app(self):
        """
        Reset the application to its initial state.
        """
        self.hero_name_entry.delete(0, tk.END)
        self.selected_powers.clear()
        self.selected_traits.clear()
        self.selected_power_listbox.delete(0, tk.END)
        self.selected_trait_listbox.delete(0, tk.END)

    def load_from_file(self):
        """
        Load hero details (powers and traits) from a JSON file.
        """
        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Open Hero File"
        )
        if not file_path:
            return  # User cancelled the open dialog

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                # Load hero name
                self.hero_name_entry.delete(0, tk.END)
                self.hero_name_entry.insert(0, data.get("hero_name", ""))
                # Load selected powers
                self.selected_powers = data.get("selected_powers", [])
                self.selected_power_listbox.delete(0, tk.END)
                for power in self.selected_powers:
                    self.selected_power_listbox.insert(tk.END, power)
                # Load selected traits
                self.selected_traits = data.get("selected_traits", [])
                self.selected_trait_listbox.delete(0, tk.END)
                for trait in self.selected_traits:
                    self.selected_trait_listbox.insert(tk.END, trait)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred while loading the file:\n{traceback.format_exc()}")

    def save_to_file(self):
        """
        Save hero details (powers and traits) to a JSON file.
        """
        hero_name = self.hero_name_entry.get().strip()
        if not hero_name:
            messagebox.showinfo("Information", "Please enter a hero name before saving.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"{hero_name}_powers_and_traits.json",
            title="Save Hero File"
        )
        if not file_path:
            return  # User cancelled the save dialog

        try:
            data = {
                "hero_name": hero_name,
                "selected_powers": self.selected_powers,
                "selected_traits": self.selected_traits
            }
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            messagebox.showinfo("Success", f"Hero details successfully saved to '{file_path}'.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred while saving the file:\n{traceback.format_exc()}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PowerAndTraitSelectionApp(root)
    root.mainloop()