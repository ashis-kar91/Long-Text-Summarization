import configparser
import openai
import PyPDF2

def extract_text_from_pdf(pdf_file_path):
    pages = []
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        for page_number in range(pdf_reader.numPages):
            text = pdf_reader.getPage(page_number).extractText()
            pages.append(text)
    return pages

def main():
    config = read_config()
    setup_openai(config)
    chatgpt_model_name = config.get('OpenAI', 'CHATGPT_MODEL')

    file_path = ''
    pages = extract_text_from_pdf(file_path)

    while pages.count > 1:
        child_pages = pages
        for page in child_pages:
            response = openai.ChatCompletion.create(
                engine=chatgpt_model_name,
                messages=[
                    {"role": "system", "content": "You are a large text summerization bot"},
                    {"role": "user", "content": "Can you summeraize this: " + page}
                    ]
                    )
            pages.append(response['choices'][0]['message']['content'])
    print(pages[0])

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