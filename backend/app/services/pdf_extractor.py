import PyPDF2
from io import BytesIO
from typing import Dict, Optional

class PDFExtractor:
    
    def extract_text(self, pdf_bytes: bytes) -> Dict[str, any]:
        try:
            pdf_file = BytesIO(pdf_bytes)
            
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            num_pages = len(pdf_reader.pages)
            
            text_content = []
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                if text.strip():  # Solo añadir si hay texto
                    text_content.append(text)
            
            # Unir todo el texto
            full_text = "\n\n".join(text_content)
            
            return {
                "success": True,
                "text": full_text,
                "num_pages": num_pages,
                "num_characters": len(full_text),
                "metadata": self._extract_metadata(pdf_reader)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "text": "",
                "num_pages": 0,
                "num_characters": 0
            }
    
    def _extract_metadata(self, pdf_reader: PyPDF2.PdfReader) -> Dict[str, Optional[str]]:
        try:
            metadata = pdf_reader.metadata
            if metadata:
                return {
                    "author": metadata.get("/Author", ""),
                    "title": metadata.get("/Title", ""),
                    "subject": metadata.get("/Subject", ""),
                    "creator": metadata.get("/Creator", "")
                }
        except:
            pass
        
        return {}