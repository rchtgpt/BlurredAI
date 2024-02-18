import openai
import os

openai.api_key = ""

def remote_call(prompt, remote_model = "gpt-3.5-turbo"):
    if (remote_model[0:3] == "gpt"):
        completion = openai.chat.completions.create(
            model=remote_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                },
            ],
        )
        response = completion.choices[0].message.content
    return response
