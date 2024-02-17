import openai
import os

def get_public_response(model, prompt):
    if(model == "GPT-3.5"):
        response = openai.Completion.create(
            engine="text-davinci-003", 
            prompt=prompt,
            temperature=0.7,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
    return response.choices[0].text.strip()