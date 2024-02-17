from openai import OpenAI
import os

TOGETHER_API_KEY = "77e2c2cf255a71c3c12c6010cb94809f705dd6321b6526a08f389c63530b60bb"

client = OpenAI(api_key=TOGETHER_API_KEY,
  base_url='https://api.together.xyz',
)

def get_local_response(model, prompt, source = "together"):
  if(source == together):
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
    response = chat_completion.choices[0].message.content
  return response