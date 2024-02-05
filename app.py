from fastapi import FastAPI, UploadFile, File
from transformers import pipeline
import pdftitle, pdfplumber
from bs4 import BeautifulSoup
from classobjects import PDF, Presentation, TextSummaryRequest, TextSummaryResponse
from pdftools import read_pdf, read_pdf_from_url, clean_text
from gemini import gemini_summarize
import requests
import pandas as pd
import difflib




pdf = PDF(textdata=None, title=None, author=None)
presentation = Presentation(title=None, author=None,
                             abstract=None, introduction=None, literature_review=None, 
                             methodology=None, results=None, conclusions=None)
model = "atulxop/presentify_finetunedt5"
summarizer = pipeline("summarization",model=model)


# pdf_path = r"C:\Users\atuls\OneDrive\Desktop\stuff\Presentify\Presentify\pdfs\A deep implicitexplicit minimizing movement method for option pricing in jumpdiffusion models.pdf"

app = FastAPI()
@app.post("/summarize", response_model=TextSummaryResponse)
async def summarize_text(request: TextSummaryRequest):
    text = request.text
    summary_text = summarizer(text, max_length=100, min_length=30)[0]["summary_text"]
    return TextSummaryResponse(summary=summary_text)

# extract title, author, textdata from pdf
@app.post('/extract-text')
async def extract_texts(file: UploadFile = File(...)):
    pdf_bytes = await file.read()

    # Optionally save the PDF temporarily
    with open('temp_pdf.pdf', 'wb') as f:
        f.write(pdf_bytes)

    extracted_text = clean_text(read_pdf('temp_pdf.pdf'))  # Replace with your program's function
    pdf_title = pdftitle.get_title_from_file('temp_pdf.pdf')
    author = pdfplumber.open('temp_pdf.pdf').metadata['Author']
    pdf.author = author
    pdf.textdata = extracted_text
    pdf.title = pdf_title

    df = gemini_summarize(pdf.textdata)
    try:
        presentation.title = pdf.title
        presentation.author = pdf.author
        presentation.introduction = df['introduction'][0]
        presentation.literature_review = df['literature review'][0]
        presentation.methodology = df['methodology'][0]
        presentation.results = df['results'][0]
        presentation.conclusions = df['conclusion'][0]
    except:
        return {'error':'couldnt extract data'}
        
    return {'title': pdf.title, 'author': pdf.author,
            'introduction':presentation.introduction,
            'literature_review':presentation.literature_review,
            'methodology':presentation.methodology,
            'results':presentation.results,
            'conclusions':presentation.conclusions
            }


@app.post("/create-presentation")
def create_presentation():
   presentation['title'] = pdf.title
   presentation['author'] = pdf.author
   return presentation

@app.post("/get_data_from_url")
async def get_data_fromI_url(arxiv_url: str):
    response = requests.get(arxiv_url)
    response = response.content
    soup = BeautifulSoup(response, 'html.parser')

    presentation.title =  soup.find('h1', class_='title mathjax').text
    presentation.author = soup.find('div', class_='authors').text
    pdf_link = arxiv_url.replace('abs', 'pdf')
    textdata = clean_text(read_pdf_from_url(pdf_link))
    presentation.title.replace('Title:','')
    presentation.author.replace('Authors:','')
    
    df = gemini_summarize(textdata)
    try:
        presentation.introduction = df['introduction'][0]
        presentation.literature_review = df['literature review'][0]
        presentation.methodology = df['methodology'][0]
        presentation.results = df['results'][0]
        presentation.conclusions = df['conclusion'][0]
    except:
        return {'error':'couldnt extract data'}
        
    return {'title': presentation.title, 'author': presentation.author,
            'introduction':presentation.introduction,
            'literature_review':presentation.literature_review,
            'methodology':presentation.methodology,
            'results':presentation.results,
            'conclusions':presentation.conclusions
            }

MAX_FILE_SIZE = 1024 * 1024 * 12  # 12MB 
@app.post('/bidhan')
async def bidhan(file: UploadFile = File(...)):
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File is too large")
    pdf_bytes = await file.read()

    # Optionally save the PDF temporarily
    with open('temp_pdf.pdf', 'wb') as f:
        f.write(pdf_bytes)

    extracted_text = clean_text(read_pdf('temp_pdf.pdf'))  # Replace with your program's function
    pdf_title = pdftitle.get_title_from_file('temp_pdf.pdf')
    author = pdfplumber.open('temp_pdf.pdf').metadata['Author']
    text = gemini_summarize(extracted_text)
    return text
    # try:
    #     presentation.title = pdf_title
    #     presentation.author = author
    #     presentation.introduction = df['introduction'][0]
    #     presentation.literature_review = df['literature review'][0]
    #     presentation.methodology = df['methodology'][0]
    #     presentation.results = df['results'][0]
    #     presentation.conclusions = df['conclusion'][0]
    # except:
    #     return {'error':'couldnt extract data'}
        
    # return {'title': presentation.title, 'author': presentation.author,
    #         'introduction':presentation.introduction,
    #         'literature_review':presentation.literature_review,
    #         'methodology':presentation.methodology,
    #         'results':presentation.results,
    #         'conclusions':presentation.conclusions
    #         }
    



