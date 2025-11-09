import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
from pathlib import Path
import csv
from tkinter import *

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from processing.invoice_ocr import InvoiceProcessor

class PreviewWindow(tk.Toplevel):
    def __init__(self, parent, csv_path):
        super().__init__(parent)
        self.title("CSV Preview")
        self.geometry("800x400")

        # Create Treeview
        self.tree = ttk.Treeview(self)
        self.tree.pack(fill=BOTH, expand=True)

        # Add scrollbars
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')

        # Load CSV data
        self.load_csv(csv_path)

    def load_csv(self, csv_path):
        with open(csv_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)
            
            # Configure columns
            self.tree["columns"] = headers
            self.tree["show"] = "headings"
            
            for header in headers:
                self.tree.heading(header, text=header)
                self.tree.column(header, width=150)
            
            # Add data
            for row in csv_reader:
                self.tree.insert("", "end", values=row)

class InvoiceProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Invoice Processor")
        self.root.geometry("800x600")
        
        self.processor = InvoiceProcessor()
        self.selected_files = {}
        self.setup_ui()
        self.preview_windows = []  # Keep track of preview windows
    
    def setup_ui(self):
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Input directory selection
        ttk.Label(self.main_frame, text="Input Directory:").grid(row=0, column=0, sticky=tk.W)
        self.input_dir_var = tk.StringVar()
        self.input_dir_entry = ttk.Entry(self.main_frame, textvariable=self.input_dir_var, width=50)
        self.input_dir_entry.grid(row=0, column=1, padx=5)
        ttk.Button(self.main_frame, text="Browse", command=self.browse_input).grid(row=0, column=2)
        
        # Output directory selection
        ttk.Label(self.main_frame, text="Output Directory:").grid(row=1, column=0, sticky=tk.W)
        self.output_dir_var = tk.StringVar()
        self.output_dir_entry = ttk.Entry(self.main_frame, textvariable=self.output_dir_var, width=50)
        self.output_dir_entry.grid(row=1, column=1, padx=5)
        ttk.Button(self.main_frame, text="Browse", command=self.browse_output).grid(row=1, column=2)
        
        # File list
        ttk.Label(self.main_frame, text="Files to process:").grid(row=2, column=0, sticky=tk.W, pady=10)
        
        # Replace the file listbox with a frame containing checkboxes
        self.files_frame = ttk.Frame(self.main_frame)
        self.files_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        # Add a canvas and scrollbar for scrolling
        self.canvas = tk.Canvas(self.files_frame, height=300)
        self.scrollbar = ttk.Scrollbar(self.files_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack the scrollbar and canvas
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Selection buttons
        self.selection_frame = ttk.Frame(self.main_frame)
        self.selection_frame.grid(row=4, column=0, columnspan=3, pady=5)
        ttk.Button(self.selection_frame, text="Select All", command=self.select_all).pack(side="left", padx=5)
        ttk.Button(self.selection_frame, text="Deselect All", command=self.deselect_all).pack(side="left", padx=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(self.main_frame, variable=self.progress_var, maximum=100)
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Process button
        self.process_btn = ttk.Button(self.main_frame, text="Process Selected Invoices", command=self.process_invoices)
        self.process_btn.grid(row=6, column=1, pady=10)
        
        # Add Preview button next to Process button
        self.preview_btn = ttk.Button(self.main_frame, text="Preview Results", command=self.preview_results)
        self.preview_btn.grid(row=6, column=2, pady=10)
    
    def browse_input(self):
        directory = filedialog.askdirectory()
        if directory:
            self.input_dir_var.set(directory)
            self.update_file_list()
            
    def browse_output(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir_var.set(directory)
            
    def update_file_list(self):
        # Clear existing checkboxes
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.selected_files.clear()
        input_dir = self.input_dir_var.get()
        
        if os.path.exists(input_dir):
            files = [f for f in os.listdir(input_dir) 
                    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp'))]
            
            for file in files:
                var = tk.BooleanVar()
                self.selected_files[file] = var
                cb = ttk.Checkbutton(self.scrollable_frame, text=file, variable=var)
                cb.pack(anchor="w", padx=5, pady=2)
    
    def select_all(self):
        for var in self.selected_files.values():
            var.set(True)
    
    def deselect_all(self):
        for var in self.selected_files.values():
            var.set(False)
    
    def process_invoices(self):
        input_dir = self.input_dir_var.get()
        output_dir = self.output_dir_var.get()
        
        if not input_dir or not output_dir:
            messagebox.showerror("Error", "Please select both input and output directories")
            return
        
        # Get selected files
        selected = [file for file, var in self.selected_files.items() if var.get()]
        
        if not selected:
            messagebox.showwarning("Warning", "Please select at least one file to process")
            return
        
        try:
            total_files = len(selected)
            for i, filename in enumerate(selected, 1):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.csv")
                self.processor.process_invoice(input_path, output_path)
                self.progress_var.set((i / total_files) * 100)
                self.root.update()
                
            # Close any existing preview windows
            for window in self.preview_windows:
                if window.winfo_exists():
                    window.destroy()
            self.preview_windows.clear()
            
            messagebox.showinfo("Success", f"Successfully processed {total_files} invoice(s)!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            self.progress_var.set(0)
    
    def preview_results(self):
        output_dir = self.output_dir_var.get()
        if not output_dir or not os.path.exists(output_dir):
            messagebox.showerror("Error", "No processed files found")
            return
            
        csv_files = [f for f in os.listdir(output_dir) if f.endswith('.csv')]
        if not csv_files:
            messagebox.showinfo("Info", "No CSV files found in output directory")
            return
            
        for csv_file in csv_files:
            csv_path = os.path.join(output_dir, csv_file)
            preview_window = PreviewWindow(self.root, csv_path)
            self.preview_windows.append(preview_window)

def main():
    root = tk.Tk()
    app = InvoiceProcessorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()