import google.generativeai as genai
import json, os
import pandas as pd
import difflib
# gemini
# response = None
title_list = ['introduction','literature review','methodology','results','conclusion']
def find_match(column_name):
  return difflib.get_close_matches(column_name, title_list)[0]
def sjoin(x): return ';'.join(x[x.notnull()].astype(str))

def gemini_summarize(textdata):
    API_KEY = 'AIzaSyAfW_f2Nc7Rs21GY-za9Nmq_syEFGDAU04' #add key here
    genai.configure(api_key= API_KEY)

    model = genai.GenerativeModel('gemini-pro')

    generation_config = genai.GenerationConfig(
    stop_sequences = None,
    temperature=0.7,
    top_p=1,
    top_k=32,
    candidate_count=1,
    max_output_tokens=1000,
    )

    if (len(textdata) <= 60000):
        while True:
            try:
                response = model.generate_content(
                '''
                Extract and provide the full content from the given research paper. Follow the instructions below:
                    - Extract content from the following segments: {"Abstract", "Introduction", "Literature Review", "Methodology", "Results", "Conclusion"} of the research paper.
                    - Ensure every line is included, without summarization or omission, and is directly related to the respective segment.
                    - Use the specified titles {"Abstract", "Introduction", "Literature Review", "Methodology", "Results", "Conclusion"} as headers; no other headings are allowed.
                    - Exclude any sections or content not relevant to the requested segments.
                    - Remove figures and tables.
                    - Format the extracted contents into a Python dictionary with the structure:
                        {"introduction": "", "literature review": "", "methodology": "", "results": "", "conclusion": ""}, strictly using double quotes ("").
                '''
                +" Here is the text:\n" + f'{textdata}'
                )
                break
            except:
                print("Error Occured while extracting using Gemini")
            #     dict={}
            # dict= json.loads(response.text)
            # df =  pd.DataFrame(dict, index=[0])
            # for column in df.columns:
            #     df[column] = df[column].astype(str)

            # for column in df.columns:
            #     try:
            #         matches = find_match(column)
            #     except:
            #         df.drop(column,axis=1)
            #     df =df.rename(columns={column:matches})
            # df = df.groupby(level=0, axis=1).apply(lambda x: x.apply(sjoin, axis=1))
    return response.text
            # break
                
from pdftools import read_pdf
text = read_pdf(r"C:\Users\atuls\Downloads\Documents\1706.03762.pdf")
print(gemini_summarize(text))