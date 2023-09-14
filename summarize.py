import configparser
import openai

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    chatgpt_model_name = config.get('OpenAI', 'CHATGPT_MODEL')
    openai.api_type = "azure"
    openai.api_key = config.get('OpenAI', "OPENAI_API_KEY")
    openai.api_base = config.get('OpenAI', 'OPENAI_API_BASE')
    openai.api_version = config.get('OpenAI', 'OPENAI_API_VERSION')

    response = openai.ChatCompletion.create(
                engine=chatgpt_model_name,
                messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": "Who won the world series in 2020?"}
                    ]
                )

    print(response['choices'][0]['message']['content'])


if __name__ == "__main__":
    main()