import os
import json
from bs4 import BeautifulSoup
from src.logger_config import get_logger

logger = get_logger()

class GrobidExtractor:
    def __init__(self, grobid_url="http://localhost:8070/api/", output_dir="data/processed"):
        self.grobid_url = grobid_url.rstrip("/")
        self.output_dir = os.path.abspath(output_dir)
        os.makedirs(self.output_dir, exist_ok=True)

    def parse_and_save_json(self, xml_content, pdf_path):
        """
        Parse GROBID TEI XML content and save structured data as JSON.
    
        Args:
            xml_content (str): XML content from GROBID.
            pdf_path (str): Path to the original PDF for naming the output file.
    
        Returns:
            str: Path to the saved JSON file.
        """
        soup = BeautifulSoup(xml_content, "lxml-xml")  # Use lxml-xml for better namespace handling
    
        # Define namespaces
        tei_ns = {"tei": "http://www.tei-c.org/ns/1.0"}
    
        # Extract metadata
        metadata = {
            "title": soup.find("title", attrs={"level": "a", "type": "main"}).get_text(strip=True) if soup.find("title", attrs={"level": "a", "type": "main"}) else None,
            "abstract": soup.find("abstract").get_text(strip=True) if soup.find("abstract") else None,
            "authors": [],
            "publication_date": soup.find("date", attrs={"type": "published"}).get("when") if soup.find("date", attrs={"type": "published"}) else None,
            "funder": [
                funder.get_text(strip=True) for funder in soup.find_all("funder")
            ],
        }
    
        # Extract authors
        for author in soup.find_all("author"):
            author_data = {
                "name": author.find("persName").get_text(strip=True) if author.find("persName") else None,
                "affiliation": [
                    {
                        "department": aff.find("orgName", attrs={"type": "department"}).get_text(strip=True) if aff.find("orgName", attrs={"type": "department"}) else None,
                        "institution": aff.find("orgName", attrs={"type": "institution"}).get_text(strip=True) if aff.find("orgName", attrs={"type": "institution"}) else None,
                        "address": {
                            "settlement": aff.find("settlement").get_text(strip=True) if aff.find("settlement") else None,
                            "region": aff.find("region").get_text(strip=True) if aff.find("region") else None,
                            "postcode": aff.find("postCode").get_text(strip=True) if aff.find("postCode") else None,
                        } if aff else None,
                    }
                    for aff in author.find_all("affiliation")
                ],
            }
            metadata["authors"].append(author_data)
    
        # Extract sections
        body = soup.find("body")
        sections = {}
        if body:
            for div in body.find_all("div"):
                section_title = div.find("head").get_text(strip=True) if div.find("head") else "Untitled Section"
                section_text = div.get_text(separator="\n", strip=True)
                sections[section_title] = section_text
    
        # Extract references
        references = []
        for ref in soup.find_all("biblStruct"):
            ref_data = {
                "title": ref.find("title").get_text(strip=True) if ref.find("title") else None,
                "authors": [
                    author.find("persName").get_text(strip=True) for author in ref.find_all("author")
                ],
                "journal": ref.find("title", attrs={"level": "j"}).get_text(strip=True) if ref.find("title", attrs={"level": "j"}) else None,
                "date": ref.find("date").get("when") if ref.find("date") else None,
                "pages": {
                    "from": ref.find("biblScope", attrs={"unit": "page", "from": True}).get("from") if ref.find("biblScope", attrs={"unit": "page", "from": True}) else None,
                    "to": ref.find("biblScope", attrs={"unit": "page", "to": True}).get("to") if ref.find("biblScope", attrs={"unit": "page", "to": True}) else None,
                },
            }
            references.append(ref_data)
    
        # Combine everything into a dictionary
        structured_data = {
            "metadata": metadata,
            "sections": sections,
            "references": references,
        }
    
        # Save as JSON
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        json_file_path = os.path.join(self.output_dir, f"{pdf_name}_data_extracted.json")
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(structured_data, json_file, indent=4)
    
        logger.info(f"Structured data saved to JSON: {json_file_path}")
        return json_file_path
    
    