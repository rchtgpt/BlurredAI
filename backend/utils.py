import json
import re
from ast import literal_eval
from prompts import get_redactor_prompt, redactor_system_prompt, get_mapper_prompt,mapper_system_prompt, get_unblur_prompt, unblur_system_prompt
from localcall import local_call
def get_dictionary_response(response):
    response_line = response.split("\n")
    flag = False
    ret = ""
    for line in response_line:
        if(line.find("{") != -1):
            flag = True
        ret += line
        if(line.find("}") != -1):
            break
    ret = ret.replace("\n", "").replace("\t", "").replace("\\", "")
    if(flag):
        try:
            return json.loads(ret)
        except:
            print("Error in parsing the response")
    print("No dictionary found in the response")
    return {}

def get_redacted_text(instruction, data_str, local_model):

    prompt = get_redactor_prompt(data_str)
    response = local_call(prompt,
                                       system_prompt=redactor_system_prompt,
                                       local_model=local_model)
    response = "".join(response).strip('```').strip()
    return response

def get_mapping(instruction, data, redacted_data, local_model):
    prompt = get_mapper_prompt(data, redacted_data)
    response = local_call(prompt,
                                       system_prompt=mapper_system_prompt,
                                       local_model=local_model)
    response = "".join(response).strip('```').strip()
    response = get_dictionary_response(response)
    if(type(response) == dict):
        return response
    else:
        return {}

def get_unblur_response(remote_response, Sensitive_mapping, local_model):
    prompt = get_unblur_prompt(remote_response, Sensitive_mapping)
    response = local_call(prompt,
                                       system_prompt=unblur_system_prompt,
                                       local_model=local_model)
    response = "".join(response).strip('```').strip()
    return response