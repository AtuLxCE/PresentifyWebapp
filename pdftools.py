import fitz
import requests
import re

def read_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path, filetype="pdf")
    text = ''
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        text += page.get_text()
    return text

def read_pdf_from_url(pdf_url):
    response = requests.get(pdf_url)
    response.raise_for_status()
    pdf_document = fitz.open(stream=response.content, filetype="pdf")
    text = ''
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        text += page.get_text()
    return text


def clean_text(text):
    text = re.sub(r'(\.\s*[^.]*)\bFig\b', '. Fig', text)
    text = re.sub(r'Table\s+(?:\S+\s+){0,5}\S*\s*.', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\S+@\S+\.\S+', '', text)
    text = re.sub(r'<.*?>', ' ', text)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'#[a-zA-Z]+', ' ', text)
    text = re.sub(r'@[a-zA-Z]+', ' ', text)
    text = re.sub(r'arXiv:\d+\.\d+v\d+ \[\w+\.\w+\] \d+ \w+\s\d+', '', text)
    text = re.sub(r'\s\d{1,2}\s', ' ', text)
    return text