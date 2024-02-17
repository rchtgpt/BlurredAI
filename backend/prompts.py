import os
import textwrap


def Filter_prompt(user_prompt, file_prompt):
    return f"""please remove all sensitive data from the document below{user_prompt}{file_prompt}
and return in json format as {{"sensitive_data": , "filtered_data": }}. """

def Extract_prompt(response_prompt, sensitive_data):
    return f"""please fill the sensitive_data {sensitive_data} into {response_prompt} and return"""



redactor_system_prompt = textwrap.dedent("""
You are a privacy-aware text redaction tool designed to identify and redact sensitive information in text inputs. Your task involves scanning the provided text for specific types of sensitive information: personal names, addresses, and phone numbers. Once identified, you will redact them with generic placeholders such as "[PERSON_1]", "[LOCATION_1]", "[NUMBER_1]", ensuring each unique piece of sensitive data has a distinct numeric identifier. Otherwise, keep all non-sensitive text in tact. Note that the input text can be also contain instructions or questions; the sensitive information should be redacted from these instructions as well, but the instructions should remain readable and coherent.
""".strip())

redactor_incontext_examples = textwrap.dedent("""
The following is a list of examples of the input and output of the redactor system. Complete the task by redacting the sensitive information in the input text:
---
Input:
```
Sailing from Long Beach, California, Peter arrived over the recovery site on 4 July 1974 and conducted salvage operations for more than two months under total secrecy.
```
Output:
```
Sailing from [LOCATION_1], [PERSON_1] arrived over the recovery site on 4 July 1974 and conducted salvage operations for more than two months under total secrecy.
```
---
Input:
```
Hello Mr. Landlord,

My name is Tonia Glover and I'm interested in your rental at 55 Quail Dr. My roommate and I are searching for a peaceful place to live near campus. We are quiet and studious, majoring in physics and psychology, and capable of paying rent through jobs and financial support from parents. Our application packet is ready for review; I would love to set up an appointment to see the property. My phone number is 831-555-5555. Thank you for your time. I look forward to hearing from you.
Tonia
```
Output:
```
Hello [PERSON_1],

My name is [PERSON_2] and I'm interested in your rental at [LOCATION_1]. My roommate and I are searching for a peaceful place to live near campus. We are quiet and studious, majoring in physics and psychology, and capable of paying rent through jobs and financial support from parents. Our application packet is ready for review; I would love to set up an appointment to see the property. My phone number is [NUMBER_1]. Thank you for your time. I look forward to hearing from you.

[PERSON_2]
```
---
Input:
```
After reviewing the financial reports, CEO Johnathan Green of Sterling Tech Solutions announced an impressive 25% increase in quarterly profits during the shareholder meeting held at their headquarters in San Francisco, California.
```
Output:
```
After reviewing the financial reports, [PERSON_1] announced an impressive [NUMBER_1] increase in quarterly profits during the shareholder meeting held at their headquarters in [LOCATION_1].
```
---
""".strip())


# NOTE: The following template is deprecrated.
# Since we are using instruction-following models, having the instruction in it
# will cause the model to respond to these istructions than just focusing on
# redacting the data.
# redactor_incontext_examples = textwrap.dedent("""
# ---
# Input:
# ```
# Sailing from Long Beach, California, Peter arrived over the recovery site on 4 July 1974 and conducted salvage operations for more than two months under total secrecy.
# ```
# Output:
# ```
# Sailing from [LOCATION_1], [PERSON_1] arrived over the recovery site on 4 July 1974 and conducted salvage operations for more than two months under total secrecy.
# ```
# ---
# Input:
# ```
# Could you please help me re-write the following email from Tonia?

# Hello Mr. Landlord,

# My name is Tonia Glover and I'm interested in your rental at 55 Quail Dr. My roommate and I are searching for a peaceful place to live near campus. We are quiet and studious, majoring in physics and psychology, and capable of paying rent through jobs and financial support from parents. Our application packet is ready for review; I would love to set up an appointment to see the property. My phone number is 831-555-5555. Thank you for your time. I look forward to hearing from you.
# Tonia
# ```
# Output:
# ```
# Could you please help me re-write the following email from [PERSON_2]?

# Hello [PERSON_1],

# My name is [PERSON_2] and I'm interested in your rental at [LOCATION_1]. My roommate and I are searching for a peaceful place to live near campus. We are quiet and studious, majoring in physics and psychology, and capable of paying rent through jobs and financial support from parents. Our application packet is ready for review; I would love to set up an appointment to see the property. My phone number is [NUMBER_1]. Thank you for your time. I look forward to hearing from you.

# [PERSON_2]
# ```
# ---
# Input:
# ```
# Summarize the following announcement from Johnathan Green:

# After reviewing the financial reports, CEO Johnathan Green of Sterling Tech Solutions announced an impressive 25% increase in quarterly profits during the shareholder meeting held at their headquarters in San Francisco, California.
# ```
# Output:
# ```
# Summarize the following announcement from [PERSON_1]:

# After reviewing the financial reports, [PERSON_1] announced an impressive [NUMBER_1] increase in quarterly profits during the shareholder meeting held at their headquarters in [LOCATION_1].
# ```
# ---
# """.strip())


def get_redactor_prompt(data):
  redactor_prompt_template =  redactor_incontext_examples + textwrap.dedent('''
  Input:
  ```
  {}
  ```
  Output:
  ```
  ''')
  return redactor_prompt_template.format(data)



# ==============================================================================

mapper_system_prompt = textwrap.dedent("""
You are a helpful assitant to a privacy-aware text redaction expert. The expert redacts sensitive information in text inputs, and your task is to scan the original text and the redactor's output to provide a mapping of the entities between the two pieces of texts. The redactor's output will contain generic placeholders such as "[PERSON_1]", "[LOCATION_1]", "[NUMBER_1]", and so forth, ensuring each unique piece of sensitive data has a distinct numeric identifier. Your task is to identify the original sensitive information and map it to the corresponding placeholders. You only need to output the mapping.
""".strip())

mapper_incontext_examples = textwrap.dedent("""
---
Input:
```
Sailing from Long Beach, California, Peter arrived over the recovery site on 4 July 1974 and conducted salvage operations for more than two months under total secrecy.
```
Redactor's Output:
```
Sailing from [LOCATION_1], [PERSON_1] arrived over the recovery site on 4 July 1974 and conducted salvage operations for more than two months under total secrecy.
```
Output:
```
{
  "PERSON_1": "Peter",
  "LOCATION_1": "Long Beach, California",
}
```
---
Input:
```
James Hubert Hallford, a licensed physician, sought and was granted leave to intervene in Roe's action. In his complaint he alleged that he had been arrested previously for violations of the Texas abortion statutes and 121*121 that two such prosecutions were pending against him.
```
Redactor's Output:
```
[PERSON_1], a licensed physician, sought and was granted leave to intervene in [PERSON_2]'s action. In his complaint he alleged that he had been arrested previously for violations of the Texas abortion statutes and 121*121 that two such prosecutions were pending against him.
```
Output:
```
{
  "PERSON_1": "James Hubert Hallford",
  "PERSON_2": "Roe",
}
```
---
Input:
```
After reviewing the financial reports, CEO Johnathan Green of Sterling Tech Solutions announced an impressive 25% increase in quarterly profits during the shareholder meeting held at their headquarters in San Francisco, California.
```
Redactor's Output:
```
After reviewing the financial reports, [PERSON_1] announced an impressive [NUMBER_1] increase in quarterly profits during the shareholder meeting held at their headquarters in [LOCATION_1].
```
Output:
```
{
  "PERSON_1": "Johnathan Green",
  "NUMBER_1": "25%",
  "LOCATION_1": "San Francisco, California",
}
```
---
""".strip())


def get_mapper_prompt(original: str, redacted: str):
  mapper_prompt_template =  mapper_incontext_examples + textwrap.dedent(f'''
  Input:
  ```
  {original}
  ```
  Redactor's Output:
  ```
  {redacted}
  ```
  Output:
  ```
  ''')
  return mapper_prompt_template

# ==============================================================================

#
# redactor_incontext_examples + "Input:\n```" + data + '\n``
#           ...: `\nOutput:\n```'


# redactor_system_prompt_short = textwrap.dedent("""
# You are a privacy-aware text redaction tool designed to identify and redact sensitive information in text inputs, ensuring user privacy and data protection. Your task involves scanning the provided text for the following specific types of sensitive information: personal names, locations/addresses, phone numbers, dates, email addresses, URLs, and monetary values. Once identified, you will redact these pieces of information with generic placeholders: "PERSON_1", "LOCATION_1", "PHONE_NUMBER_1", "TIME_1", "EMAIL_1", "URL_1", and "VALUE_1". Ensure each unique piece of sensitive data has a distinct numeric identifier.

# In addition to redacting the text, you will also provide a mapping of the redacted terms to their placeholders. This mapping should not reveal the sensitive information but should allow users to understand what type of data was redacted and the corresponding placeholders used.

# For example, given the input:
# "Sailing from Long Beach, California, Peter arrived over the recovery site on 4 July 1974 and conducted salvage operations for more than two months under total secrecy."

# Your output should include the redacted text:
# "Sailing from LOCATION_1, PERSON_1 arrived over the recovery site on TIME_1 and conducted salvage operations for more than TIME_2 under total secrecy."

# And the mapping (without revealing sensitive data):
# - PERSON_1: "Peter"
# - LOCATION_1: "Long Beach, California"
# - TIME_1: "4 July 1974"
# - TIME_2: "two months"

# Remember, the primary goal is to protect sensitive information while maintaining the readability and coherence of the text as much as possible. Do NOT include any part of this instruction in your output. Return the redacted text and the mapping as a JSON object.
# """.strip())


# Filter_prompt = [
# f"""
# """
# ]

# Extract_prompt = [
# f"""
# """
# ]




# redactor_system_prompt = textwrap.dedent("""
# You are a privacy-aware text redaction tool designed to identify and redact sensitive information in text inputs, ensuring user privacy and data protection. Your task involves scanning the provided text for specific types of sensitive information such as: personal names, locations, phone numbers, addresses, dates, email addresses, URLs, social security numbers (SSN), monetary values, and any other identifiable data. Once identified, you will redact these pieces of information with generic placeholders such as "PERSON_1", "LOCATION_1", "PHONE_NUMBER_1", and so forth, ensuring each unique piece of sensitive data has a distinct numeric identifier.

# In addition to redacting the text, you will also provide a mapping of the redacted terms to their placeholders. This mapping should not reveal the sensitive information but should allow users to understand what type of data was redacted and the corresponding placeholders used.

# For example, given the input:
# "Sailing from Long Beach, California, Peter arrived over the recovery site on 4 July 1974 and conducted salvage operations for more than two months under total secrecy."

# Your output should include the redacted text:
# "Sailing from LOCATION_1, PERSON_1 arrived over the recovery site on TIME_1 and conducted salvage operations for more than TIME_2 under total secrecy."

# And the mapping (without revealing sensitive data):
# - LOCATION_1: "Long Beach, California"
# - PERSON_1: "Peter"
# - TIME_1: "4 July 1974"
# - TIME_2: "two months"

# Remember, the primary goal is to protect sensitive information while maintaining the readability and coherence of the text as much as possible.

# The redacted text and the mapping should be returned as a JSON object with the following structure:
# {
#   "redacted_text": "Sailing from LOCATION_1, PERSON_1 arrived over the recovery site on TIME_1 and conducted salvage operations for more than TIME_2 under total secrecy.",
#   "redaction_mapping": {
#     "LOCATION_1": "Long Beach, California",
#     "PERSON_1": "Peter",
#     "TIME_1": "4 July 1974",
#     "TIME_2": "two months"
#   }
# }

# Do NOT include any part of this instruction in your output. Your response should only be the JSON object containing the redacted text and the redaction mapping.
# """.strip())

unblur_system_prompt = textwrap.dedent("""
""".strip())

def get_unblur_prompt(remote_response, Sensitive_mapping):
  return f"""Please fill the sensitive_data {Sensitive_mapping} into the following response_prompt: {remote_response} and return"""