import configparser
import openai
import PyPDF2
import time
import tiktoken


def extract_text_from_pdf(pdf_file_path):
    pages = []
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            pages.append(text)
    return pages


def main():
    file_path = r"input_files\transcript-q1pdf.pdf"
    pages = extract_text_from_pdf(file_path)

    config = read_config()
    setup_openai(config)
    chatgpt_model_name = config.get('OpenAI', 'CHATGPT_MODEL')

    encoding = tiktoken.encoding_for_model("gpt-35-turbo-16k")
    total_tokens = 0
    exe_count = 0
    page_input = ""
    summary_page = ""
    page_carry = ""
    pagescopy = pages
    while(len(pagescopy) > 0):
        pages = pagescopy
        pagescopy = []
        for page in pages:
            if(page_carry != ""):
                page_input += page_carry
                page_carry = ""
            token_count = len(encoding.encode(page))
            total_tokens += token_count
            if(total_tokens < 16000):
                page_input += page
            else:
                response = get_summary(chatgpt_model_name, page_input)
                summary_page += response['choices'][0]['message']['content']
                exe_count += 1
                print(exe_count)
                if(exe_count % 3 == 0):
                    time.sleep(60)
                    pagescopy.append(summary_page)
                    summary_page = ""
                page_input = ""
                page_carry = page
                total_tokens = token_count
        if(page_input != ""):
            response = get_summary(chatgpt_model_name, page_input)
            summary_page += response['choices'][0]['message']['content']
            exe_count += 1
            print(exe_count)
            if(exe_count % 3 == 0):
                pagescopy.append(summary_page)
                summary_page = ""
        if(summary_page != ""):
            pagescopy.append(summary_page)
        if(len(pagescopy) == 1):
            break
    print(pagescopy[0])

def get_summary(chatgpt_model_name, page_input):
    return openai.ChatCompletion.create(
                    engine=chatgpt_model_name,
                    messages=[
                            {"role": "system", "content": "You are a large text summerization bot"},
                            {"role": "user", "content": "Can you summeraize this: " + page_input}
                        ],
                    temperature=0.2
                    )


def setup_openai(config):
    openai.api_type = "azure"
    openai.api_key = config.get('OpenAI', "OPENAI_API_KEY")
    openai.api_base = config.get('OpenAI', 'OPENAI_API_BASE')
    openai.api_version = config.get('OpenAI', 'OPENAI_API_VERSION')


def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config


if __name__ == "__main__":
    main()
