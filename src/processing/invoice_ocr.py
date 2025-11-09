import os
from paddleocr import PaddleOCR
import csv
import re
from typing import List, Tuple, Dict

class InvoiceProcessor:
    """
    A class to process invoice images and extract structured data into CSV format.
    
    Attributes:
        ocr (PaddleOCR): The OCR engine instance for text recognition
    """
    def __init__(self, lang='fr'):
        print("Initializing OCR engine...")
        self.ocr = PaddleOCR(lang=lang, use_textline_orientation=True)
        
    def process_directory(self, input_dir: str, output_dir: str) -> None:
        """Process all images in directory"""
        os.makedirs(output_dir, exist_ok=True)
        
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.csv")
                self.process_invoice(input_path, output_path)

    def process_invoice(self, image_path: str, output_path: str) -> None:
        """Process single invoice"""
        print(f"Processing {image_path}...")
        try:
            results = self.ocr.predict(image_path)
            rows = self.extract_table_rows(results)
            if rows:
                self.save_to_csv(rows, output_path)
                print(f"Successfully saved to {output_path}")
            else:
                print(f"No valid data found in {image_path}")
        except Exception as e:
            print(f"Error processing {image_path}: {str(e)}")

    def extract_table_rows(self, results: List) -> List[Tuple]:
        """Extract and structure table data"""
        text_boxes = []
        
        # Extract text and coordinates
        if isinstance(results, list):
            for item in results:
                if isinstance(item, dict) and 'rec_texts' in item:
                    for idx, text in enumerate(item['rec_texts']):
                        if 'rec_boxes' in item and len(item['rec_boxes']) > idx:
                            box = item['rec_boxes'][idx]
                            y_coord = sum(box[1::2]) / 2
                            x_coord = sum(box[0::2]) / 2
                            text_boxes.append((y_coord, x_coord, text.strip()))

        # Sort and group by Y coordinate
        text_boxes.sort(key=lambda x: (x[0], x[1]))
        rows = self.group_into_rows(text_boxes)
        
        # Process rows into structured data
        invoice_rows = []
        for row in rows:
            processed_row = self.process_row(row)
            if processed_row:
                invoice_rows.append(processed_row)
        
        return invoice_rows

    def group_into_rows(self, text_boxes: List[Tuple], y_threshold: int = 15) -> List[List[str]]:
        """Group text boxes into rows based on Y-coordinate"""
        rows = []
        current_row = []
        last_y = None
        
        for y, x, text in text_boxes:
            if last_y is None or abs(y - last_y) > y_threshold:
                if current_row:
                    rows.append(sorted(current_row, key=lambda x: x[1]))
                current_row = []
                last_y = y
            current_row.append((y, x, text))
        
        if current_row:
            rows.append(sorted(current_row, key=lambda x: x[1]))
            
        return [[text for _, _, text in row] for row in rows]

    def process_row(self, row: List[str]) -> Tuple[str, str, str, str]:
        """Process a row into (designation, quantity, price, amount)"""
        if len(row) < 2:
            return None
            
        # Extract numbers and text
        numbers = []
        text_parts = []
        
        for item in row:
            num = self.parse_number(item)
            if num is not None:
                numbers.append(num)
            elif self.is_valid_text(item):
                text_parts.append(item)
        
        # Validate and structure the row
        if len(numbers) >= 2 and text_parts:
            designation = ' '.join(text_parts).strip()
            if len(numbers) >= 3:
                return (
                    designation,
                    str(int(numbers[0]) if numbers[0].is_integer() else numbers[0]),
                    f"{numbers[1]:.2f}",
                    f"{numbers[2]:.2f}"
                )
            else:
                return (
                    designation,
                    "",
                    f"{numbers[0]:.2f}",
                    f"{numbers[1]:.2f}"
                )
        return None

    def parse_number(self, text: str) -> float:
        """Parse number from text, handling French number format"""
        try:
            # Remove spaces and handle comma as decimal separator
            clean = text.replace(' ', '').replace(',', '.')
            return float(clean)
        except ValueError:
            return None

    def is_valid_text(self, text: str) -> bool:
        """Check if text is valid designation"""
        if not text.strip():
            return False
        invalid_starts = ('N°', 'Tel', 'R.', 'C.', 'Sous', 'Total', 'TVA')
        return not any(text.strip().startswith(x) for x in invalid_starts)

    def save_to_csv(self, rows: List[Tuple], output_path: str) -> None:
        """Save processed rows to CSV"""
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Designation', 'Quantité', 'Prix Unitaire', 'Montant'])
            writer.writerows(rows)