import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import pandas as pd
import numpy as np
import copy

class DataCleanerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Data Cleaner App")
        
        # Set custom icon
        self.iconbitmap(default='GUIicon.ico')

        # Left Frame for buttons
        self.left_frame = tk.Frame(self, width=200, bg='light gray')
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Main Frame for data display
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Buttons
        self.buttons = {
            "Read": self.read_file,
            "Identify Missing Values": self.identify_missing_values,
            "Drop Missing Values": self.drop_missing_values,
            "Identify Duplicates": self.identify_duplicates,
            "Drop Duplicates": self.drop_duplicates,
            "Check Data Format": self.check_data_format,
            "Drop Rows with Special Characters": self.drop_special_characters,
            "Select Columns to Drop": self.select_columns_to_drop,
            "Export Cleaned Data": self.export_cleaned_data,
            "Update/Refresh": self.update_display,
            "Reverse Changes": self.reverse_changes
        }
        for text, command in self.buttons.items():
            tk.Button(self.left_frame, text=text, command=command).pack(fill=tk.X, padx=10, pady=5)

        # Text widget to display data
        self.data_text = tk.Text(self.main_frame, wrap=tk.NONE)
        self.data_text.pack(expand=True, fill=tk.BOTH)

        self.df = None  # Dataframe to store loaded data
        self.original_df = None  # Store a copy of the original dataframe for rollback

    def read_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
        if file_path:
            try:
                # Read data from file
                if file_path.endswith('.csv'):
                    self.df = pd.read_csv(file_path)
                elif file_path.endswith('.xlsx'):
                    self.df = pd.read_excel(file_path)
                else:
                    raise ValueError("Unsupported file format")

                # Save a copy of the original dataframe
                self.original_df = copy.deepcopy(self.df)

                # Display data in the Text widget
                self.update_display()
            except Exception as e:
                self.data_text.delete(1.0, tk.END)  # Clear previous content
                self.data_text.insert(tk.END, f"Error reading file: {e}")

    def identify_missing_values(self):
        if self.df is not None:
            missing_values = self.df.isna().sum()
            self.data_text.delete(1.0, tk.END)
            self.data_text.insert(tk.END, f"Missing Values:\n{missing_values}")

    def drop_missing_values(self):
        if self.df is not None:
            confirmed = messagebox.askyesno("Confirm Drop", "Are you sure you want to drop missing values?")
            if confirmed:
                self.df.dropna(inplace=True)
                self.update_display()

    def identify_duplicates(self):
        if self.df is not None:
            duplicates = self.df[self.df.duplicated()]
            self.data_text.delete(1.0, tk.END)
            self.data_text.insert(tk.END, "Duplicate Rows:\n")
            self.data_text.insert(tk.END, duplicates.to_string(index=False))

    def drop_duplicates(self):
        if self.df is not None:
            confirmed = messagebox.askyesno("Confirm Drop", "Are you sure you want to drop duplicates?")
            if confirmed:
                self.df.drop_duplicates(inplace=True)
                self.update_display()

    def check_data_format(self):
        if self.df is not None:
            data_types = self.df.dtypes
            self.data_text.delete(1.0, tk.END)
            self.data_text.insert(tk.END, "Data Format:\n")
            self.data_text.insert(tk.END, data_types.to_string())

    def drop_special_characters(self):
        if self.df is not None:
            confirmed = messagebox.askyesno("Confirm Drop", "Are you sure you want to drop rows with special characters?")
            if confirmed:
                self.df = self.df.replace(regex=r'[^\w\d\s]', value=np.nan)
                self.update_display()

    def select_columns_to_drop(self):
        if self.df is not None:
            columns = self.df.columns
            selected_columns = simpledialog.askstring("Select Columns to Drop", f"Enter column names to drop (comma-separated):\n{', '.join(columns)}")
            if selected_columns:
                selected_columns = [col.strip() for col in selected_columns.split(',')]
                confirmed = messagebox.askyesno("Confirmation", f"Are you sure you want to drop columns: {', '.join(selected_columns)}?")
                if confirmed:
                    self.df.drop(columns=selected_columns, inplace=True)
                    self.update_display()

    def export_cleaned_data(self):
        if self.df is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                try:
                    self.df.to_csv(file_path, index=False)
                    self.data_text.delete(1.0, tk.END)
                    self.data_text.insert(tk.END, f"Cleaned data saved to {file_path}")
                except Exception as e:
                    self.data_text.delete(1.0, tk.END)
                    self.data_text.insert(tk.END, f"Error saving file: {e}")

    def update_display(self):
        if self.df is not None:
            self.data_text.delete(1.0, tk.END)
            self.data_text.insert(tk.END, self.df.to_string(index=False))

    def reverse_changes(self):
        if self.original_df is not None:
            self.df = copy.deepcopy(self.original_df)
            self.update_display()

if __name__ == "__main__":
    app = DataCleanerApp()
    app.mainloop()
