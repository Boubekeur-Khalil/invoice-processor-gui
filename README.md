# Invoice Processor GUI

A Python GUI application for processing invoices using OCR and converting them to CSV format.

## Features

- User-friendly GUI interface
- Process multiple invoice images at once
- Preview CSV results in tabular format
- Supports multiple image formats (PNG, JPG, JPEG, TIFF, BMP)
- Progress tracking
- Batch selection tools

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Boubekeur-Khalil/invoice-processor-gui.git
cd invoice-processor-gui
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:

```bash
python -m src.gui.main_window
```

2. Select input directory containing invoice images
3. Choose output directory for CSV files
4. Select the invoices you want to process
5. Click "Process Selected Invoices"
6. Use "Preview Results" to view the extracted data

## Author

Boubekeur Khalil
- GitHub: [@Boubekeur-Khalil](https://github.com/Boubekeur-Khalil)

## License

MIT License