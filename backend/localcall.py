from openai import OpenAI
import os

from prompts import redactor_system_prompt

TOGETHER_API_KEY = "77e2c2cf255a71c3c12c6010cb94809f705dd6321b6526a08f389c63530b60bb"


def get_local_response(model, prompt, source = "together"):
  if(source == "together"):
    chat_completion = client.chat.completions.create(
      messages=[
        {
          "role": "system",
          "content": "You are an AI assistant",
        },
        {
          "role": "user",
          "content": prompt,
        }
      ],
      model=model,
      max_tokens=1024
    )
    return response


def together_call(prompt: str, model='mistralai/Mixtral-8x7B-Instruct-v0.1', max_tokens=1024):
    client = OpenAI(
        api_key=TOGETHER_API_KEY,
        base_url='https://api.together.xyz',

    )

    messages = [{
        "role": "system",
        "content": "You are an AI assistant",
    }, {
        "role": "user",
        "content": prompt,
    }]
    chat_completion = client.chat.completions.create(messages=messages,
                                                     model=model,
                                                     max_tokens=max_tokens)
    response = chat_completion.choices[0].message.content

    return response



def together_call_streaming(prompt: str,
                            system_prompt: str,
                            model='mistralai/Mixtral-8x7B-Instruct-v0.1',
                            max_tokens=1024):
    client = OpenAI(
        api_key=TOGETHER_API_KEY,
        base_url='https://api.together.xyz',
    )

    messages = [{
        "role": "system",
        "content": system_prompt,
    }, {
        "role": "user",
        "content": prompt,
    }]
    stream = client.chat.completions.create(messages=messages,
                                            model=model,
                                            max_tokens=max_tokens,
                                            stream=True,
                                            # response_format={ "type": "json_object" },
                                            )
    for chunk in stream:
        response = chunk.choices[0].delta.content
        print(response, end='', flush=True)

    # json = stream
    # return json




if __name__ == "__main__":
  print(get_local_response("mistralai/Mixtral-8x7B-Instruct-v0.1", """please remove all sensitive data from the document below"my name is jojo, I am 24 years old"
. Return in json format as {"sensitive_data": , "filtered_data": }. """))

