import openai
import sys
import time
import operator as op
from PyPDF2 import PdfReader


config = {
    "CHATGPT_MODEL":"",
    "OPENAI_API_BASE":"",
    "OPENAI_API_VERSION":"",
    "OPENAI_API_KEY" : ""
}

QUERY_LIMIT = 3
DELAY_SECS = 60
QUERY_LENGTH = 16000

def pdfToTextGenerator(filename):  
    reader = PdfReader(filename)
    
    print("Number of pages: "+str(len(reader.pages)))

    pages = []
    for page in reader.pages:
        pages.append(page.extract_text())
    return pages

def openai_summarize_text(text):
    # Setting up the deployment name
    chatgpt_model_name = config['CHATGPT_MODEL']
    openai.api_type = "azure"
    openai.api_key = config["OPENAI_API_KEY"]
    openai.api_base = config['OPENAI_API_BASE']
    openai.api_version = config['OPENAI_API_VERSION']

    response = openai.ChatCompletion.create(
                engine=chatgpt_model_name,
                messages=[
                        {"role": "user", "content": "can you summarize: "+text}
                    ],
                temperature=0
                )

    return response['choices'][0]['message']['content']

def summarize_local(summarize_in):
    summarize_out = []
    text_concat = ""
    query_count = 0
    for text in summarize_in:
        token_count1 = op.countOf(text_concat, " ")
        token_count2 = op.countOf(text, " ")
        if(token_count1 + token_count2 + 1 < QUERY_LENGTH):
            text_concat = text_concat + "\n" + text
        else:
            if(query_count >= QUERY_LIMIT):
                print("sleep")
                time.sleep(DELAY_SECS)
                query_count = 0
            response = openai_summarize_text(text)
            summarize_out.append(response)
            query_count += 1
            text_concat = text
    if(len(text_concat) > 0 and not text_concat.isspace()):
        if(query_count >= QUERY_LIMIT):
            print("sleep")
            time.sleep(DELAY_SECS)
            query_count = 0
        response = openai_summarize_text(text)
        summarize_out.append(response)
        query_count += 1
    return summarize_out



def summarize(filename):
    pages = pdfToTextGenerator(filename)
    summarize_out = pages
    while(len(summarize_out) > 1):
        print("Summarize length: "+str(len(summarize_out)))
        summarize_out = summarize_local(summarize_out)
    return summarize_out[0]
        
def main(argv):
    result = summarize(argv[0])
    print(result)

if __name__ == "__main__":
    main(sys.argv[1:])