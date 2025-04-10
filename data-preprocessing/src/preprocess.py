import os
import requests
from src.grobid_extractor import GrobidExtractor
from src.logger_config import get_logger
from src.pdf_loader import PDFLoader
from src.text_cleaner import TextCleaner  # New import
import json

from dotenv import load_dotenv

load_dotenv()
logger = get_logger()

def get_file_path(sub_dir, file_name):
    """
    Constructs the full path to a file based on the project root directory.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base_dir, sub_dir, file_name)

def run_pdf_loading():
    """
    Step 1: Load PDFs from S3 using PDFLoader and save them to the raw data directory.
    """
    logger.info("Initializing PDFLoader...")
    loader = PDFLoader()

    # Fetch PDFs from S3 (limit = 3)
    logger.info("Fetching PDFs from S3...")
    try:
        pdfs = loader.fetch_pdfs_from_s3(limit=10)  # Use the method in PDFLoader
        for file_name, pdf_content in pdfs:
            # Save each PDF to the raw data directory
            output_path = get_file_path("data/raw", os.path.basename(file_name))
            logger.info(f"Saving PDF to {output_path}...")
            with open(output_path, "wb") as f:
                f.write(pdf_content)
            logger.info(f"PDF saved successfully to {output_path}")
    except Exception as e:
        logger.error(f"Error during PDF loading: {e}")

def run_grobid_extraction():
    """
    Step 2: Extract structured content from all PDFs in the raw data directory using GROBID.
    """
    logger.info("Initializing GrobidExtractor...")
    grobid_extractor = GrobidExtractor(output_dir=get_file_path("data", "processed"))

    # Directory containing the raw PDFs
    raw_pdf_dir = get_file_path("data", "raw")
    grobid_url = "http://localhost:8070/api/processFulltextDocument"

    # List all PDF files in the raw directory
    pdf_files = [f for f in os.listdir(raw_pdf_dir) if f.endswith(".pdf")]

    if not pdf_files:
        logger.warning("No PDF files found in the raw data directory.")
        return

    logger.info(f"Found {len(pdf_files)} PDFs in {raw_pdf_dir}. Starting GROBID extraction...")

    for pdf_file in pdf_files:
        pdf_path = os.path.join(raw_pdf_dir, pdf_file)
        logger.info(f"Processing PDF: {pdf_path}")

        try:
            with open(pdf_path, "rb") as pdf:
                # Send the PDF to GROBID for processing
                response = requests.post(
                    grobid_url,
                    files={"input": pdf},
                    headers={"Accept": "application/xml"}
                )

            if response.status_code == 200:
                logger.info(f"Successfully processed {pdf_file}. Parsing XML and saving as JSON...")
                xml_content = response.text
                grobid_extractor.parse_and_save_json(xml_content, pdf_path)
            else:
                logger.error(f"GROBID API failed for {pdf_file} with status {response.status_code}: {response.text}")
        except Exception as e:
            logger.error(f"Error during GROBID extraction for {pdf_file}: {e}")

    logger.info("GROBID extraction completed for all PDFs.")


def run_text_cleaning():
    """
    Step 3: Clean and index sections dynamically from all extracted JSON files and save them to MongoDB.
    """
    logger.info("Initializing TextCleaner...")
    cleaner = TextCleaner(
        mongo_uri= os.getenv("MONGO_URI"),
        mongo_db= os.getenv("MONGO_DB"),
        mongo_collection=os.getenv("MONGO_COLLECTION")
    )

    # Directory containing the extracted JSON files
    input_json_dir = get_file_path("data", "processed")
    json_files = [f for f in os.listdir(input_json_dir) if f.endswith(".json")]

    if not json_files:
        logger.warning("No JSON files found in the processed data directory.")
        return

    logger.info(f"Found {len(json_files)} JSON files in {input_json_dir}. Starting cleaning and saving to MongoDB...")

    for json_file in json_files:
        input_json_path = os.path.join(input_json_dir, json_file)
        logger.info(f"Processing JSON file: {input_json_path}")

        try:
            # Load the JSON file
            with open(input_json_path, "r", encoding="utf-8") as file:
                json_data = json.load(file)

            # Clean and save to MongoDB
            cleaner.clean_and_save_to_mongo(json_data)

        except Exception as e:
            logger.error(f"Failed to process JSON file {json_file}: {e}")

    logger.info("Completed cleaning and saving all JSON files to MongoDB.")


def main():
    """
    Main menu-driven function to execute preprocessing steps.
    """
    while True:
        print("\nPreprocessing Steps Menu:")
        print("1. Load PDF using PDFLoader")
        print("2. Extract Structured Content with GROBID")
        print("3. Clean and Index Extracted Sections")
        print("4. Exit")

        choice = input("Enter the step number to execute: ").strip()

        if choice == "1":
            logger.info("Running Step 1: Load PDF...")
            run_pdf_loading()
        elif choice == "2":
            logger.info("Running Step 2: Structured Content Extraction...")
            run_grobid_extraction()
        elif choice == "3":
            logger.info("Running Step 3: Clean and Index Extracted Sections...")
            run_text_cleaning()
        elif choice == "4":
            logger.info("Exiting the preprocessing pipeline.")
            break
        else:
            print("Invalid choice. Please select a valid step.")

if __name__ == "__main__":
    main()
