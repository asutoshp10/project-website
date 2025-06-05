import resume_analyzer
import pdfplumber
from pdf2image import convert_from_path
import pytesseract
import re

class Resume_scorer():
    def __init__(self,path=r'',job='No'):
        self.path=path
        self.text=''
        self.job=job

    def extract_text_from_pdf(self):
        try:
            with pdfplumber.open(self.path) as pdf:
                for pages in pdf.pages:
                    page_text=pages.extract_text()
                    if page_text:
                        self.text+=page_text
        except Exception as e:
            print('Cant parse pdf by pdfplumber')
        
        if self.text.strip():
            return self.text.strip()
        
        try:
            images=convert_from_path(self.path)
            for pages in images:
                page_text=pytesseract.image_to_string(pages)
                self.text+=page_text+'\n'
        except Exception as e:
            print(f'OCR Failed {e}')
        
        return self.text.strip()
    


    def parse_analyse(self):
        analysis=resume_analyzer.analyze_resume(self.text,self.job)
        return analysis
    
    def extract_contacts(self,text):
        # Email pattern
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

        # Phone pattern (flexible, catches many formats)
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?(\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{4}'

        emails = re.findall(email_pattern, text)
        phones = re.findall(phone_pattern, text)

        # Format phone numbers nicely
        phones = [''.join(p) for p in phones if ''.join(p).strip()]

        return emails, phones

# r=Resume_scorer(r'C:\Users\asuto\Desktop\AI proj\Assets\123ME0421 Asutosh Resume.pdf')
# r.extract_text_from_pdf()
# print(r.parse_analyse())