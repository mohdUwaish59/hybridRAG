import os
from pdfminer.high_level import extract_text
from loguru import logger

class PDFTextExtractor:
    def __init__(self, output_dir="data/processed"):
        """
        Initialize the PDF text extractor.

        Args:
            output_dir (str): Directory to save extracted text files.
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        logger.info(f"PDFTextExtractor initialized. Output directory: {self.output_dir}")

    def extract_text(self, pdf_path):
        """
        Extracts raw text from a PDF file.

        Args:
            pdf_path (str): Path to the PDF file.

        Returns:
            str: Extracted text.
        """
        if not os.path.exists(pdf_path):
            logger.error(f"PDF file not found: {pdf_path}")
            return ""

        try:
            logger.info(f"Extracting text from {pdf_path}...")
            text = extract_text(pdf_path)
            logger.info("Text extraction completed.")
            return text
        except Exception as e:
            logger.error(f"Error during text extraction: {e}")
            return ""

    def save_text(self, text, output_filename):
        """
        Saves the extracted text to a file.

        Args:
            text (str): Extracted text content.
            output_filename (str): Name of the output text file.

        Returns:
            str: Path to the saved text file.
        """
        output_path = os.path.join(self.output_dir, output_filename)
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)
            logger.info(f"Extracted text saved to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error saving text to file: {e}")
            return None

    def process_pdf(self, pdf_path, output_filename):
        """
        Complete text extraction and saving process for a PDF.

        Args:
            pdf_path (str): Path to the PDF file.
            output_filename (str): Name of the output text file.

        Returns:
            str: Path to the saved text file.
        """
        text = self.extract_text(pdf_path)
        if text:
            return self.save_text(text, output_filename)
        else:
            logger.error("No text extracted. Skipping save operation.")
            return None
