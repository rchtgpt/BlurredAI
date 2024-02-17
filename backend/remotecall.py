import openai
import os

openai.api_key = "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"

def remote_call(prompt, model = "gpt-3.5-turbo"):
    if (model == "gpt-3.5-turbo"):
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                },
            ],
        )
        response = completion.choices[0].message.content
    return response
