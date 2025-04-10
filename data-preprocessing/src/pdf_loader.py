import os
import boto3
from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env
load_dotenv()


class PDFLoader:
    def __init__(self):
        """
        Initializes the PDFLoader instance with S3 configuration from environment variables.
        """
        self.bucket_name = os.getenv("AWS_S3_BUCKET")
        self.region_name = os.getenv("AWS_REGION")

        if not self.bucket_name or not self.region_name:
            raise ValueError("AWS S3 bucket name or region is not set in the .env file.")

        self.s3_client = boto3.client("s3", region_name=self.region_name)
        logger.info(f"PDFLoader initialized with bucket: {self.bucket_name} in region: {self.region_name}")

    def fetch_pdfs_from_s3(self, limit):
        """
        Fetches up to `limit` PDF files from the specified S3 bucket.

        Args:
            limit (int): The maximum number of PDFs to fetch.

        Returns:
            list: A list of tuples containing the S3 file key and its content.
        """
        logger.info(f"Fetching up to {limit} PDFs from S3 bucket: {self.bucket_name}")

        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
            if "Contents" not in response:
                logger.error("No files found in the S3 bucket.")
                return []

            # Filter for PDF files and limit the number of files
            pdf_keys = [obj["Key"] for obj in response["Contents"] if obj["Key"].endswith(".pdf")][:limit]

            pdfs = []
            for key in pdf_keys:
                logger.info(f"Downloading PDF from S3: {key}")
                pdf_object = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)
                pdfs.append((key, pdf_object["Body"].read()))

            logger.info(f"Successfully downloaded {len(pdfs)} PDFs from S3.")
            return pdfs
        except Exception as e:
            logger.error(f"Error fetching PDFs from S3: {e}")
            return []

    def save_pdf(self, pdf_content, output_path):
        """
        Saves the PDF content to a specified file.

        Args:
            pdf_content (bytes): The PDF content.
            output_path (str): The path to save the PDF file.

        Returns:
            bool: True if the file is saved successfully, False otherwise.
        """
        if not pdf_content:
            logger.error("No content to save. Skipping save operation.")
            return False

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        try:
            with open(output_path, "wb") as f:
                f.write(pdf_content)
            logger.info(f"PDF saved successfully to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving PDF to {output_path}: {e}")
            return False
