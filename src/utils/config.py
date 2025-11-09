# filepath: /invoice-processor-gui/invoice-processor-gui/src/utils/config.py
# Configuration settings and constants for the invoice processing application

# GUI Configuration
WINDOW_TITLE = "Invoice Processor"
WINDOW_SIZE = "800x600"

# File Processing Configuration
SUPPORTED_IMAGE_FORMATS = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']
OUTPUT_CSV_HEADER = ['Designation', 'Quantité', 'Prix Unitaire', 'Montant']

# OCR Configuration
OCR_LANGUAGE = 'fr'
USE_TEXTLINE_ORIENTATION = True

# Directories
INPUT_DIRECTORY = "input_invoices"
OUTPUT_DIRECTORY = "processed_invoices"