from openai import OpenAI
import os

TOGETHER_API_KEY = ""

def local_call(prompt, system_prompt = "You are an AI assistant", local_model = "mistralai/Mixtral-8x7B-Instruct-v0.1", streaming = False, source = "together", max_tokens = 1024, response_format = None):
   if source == "together":
      return together_call(prompt = prompt, system_prompt = system_prompt, local_model = local_model)
   else:
      return ""
   
def together_call(prompt, system_prompt, local_model, streaming = False, max_tokens = 1024, response_format = None):
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
    if response_format == None:
      chat_completion = client.chat.completions.create(messages=messages,
                                                      model=local_model,
                                                      max_tokens=max_tokens,
                                                      #response_format={ "type": "json_object" },
                                                      stream=streaming)
    else:
      chat_completion = client.chat.completions.create(messages=messages,
                                                      model=local_model,
                                                      max_tokens=max_tokens,
                                                      response_format={ "type": "json_object" },
                                                      stream=False)
    response = chat_completion.choices[0].message.content
    return response



if __name__ == "__main__":
  data = """Hello Mr. Landlord, My name is Tonia Glover and I'm interested in your rental at 55 Quail Dr. My roommate and I are searching for a peaceful place to live near campus. We are quiet and studious, majoring in physics and psychology, and capable of paying rent through jobs and financial support from parents. Our application packet is ready for review; I would love to set up an appointment to see the property. My phone number is 831-555-5555. 
Thank you for your time. I look forward to hearing from you.Tonia"""

