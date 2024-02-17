import openai
import os

openai.api_key = "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"
def get_public_response(model, prompt):
    if(model == "GPT-3.5-turbo"):
        model_response = openai.Completion.create(
            engine="GPT-3.5-turbo", 
            prompt=prompt,
            temperature=0.7,
            max_tokens=200,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        response = model_response.choices[0].text.strip()
    return response