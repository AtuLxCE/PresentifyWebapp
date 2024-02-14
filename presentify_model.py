from classobjects import PresentationData
from transformers import pipeline
import nltk
# from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# nltk.download('stopwords')
# nltk.download('punkt')
stop_words = ['a','an','the']

model = "atulxop/deployment_model"
summarizer = pipeline("summarization",model=model)
def wordcount(text, count=0):
    for word in text.split():
        count += 1
    return count

def sent_summarizer(text):
    sentences = [sentence for sentence in text.split('.')]
    for sentence in sentences:
        if wordcount(sentence) > 15:
            summarized_sent = summarizer(sentence)[0]["summary_text"]
            text = text.replace(sentence+'.', summarized_sent)
            return text
def remove_stopwords(text):
    words = word_tokenize(text)
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return " ".join(filtered_words)
            
def summarize(prs: PresentationData):
    prs.introduction = summarizer(prs.introduction)[0]["summary_text"]
    prs.introduction = remove_stopwords(prs.introduction)
    prs.literature_review = summarizer(prs.literature_review)[0]["summary_text"]
    prs.literature_review = remove_stopwords(prs.literature_review)
    prs.methodology = summarizer(prs.methodology)[0]["summary_text"]
    prs.methodology = remove_stopwords(prs.methodology)
    prs.results = summarizer(prs.results)[0]["summary_text"]
    prs.results = remove_stopwords(prs.results)
    prs.conclusions = summarizer(prs.conclusions)[0]["summary_text"]
    prs.conclusions = remove_stopwords(prs.conclusions)
    return prs