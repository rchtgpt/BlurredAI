import json
import re
from ast import literal_eval
from prompts import get_redactor_prompt, redactor_system_prompt, get_mapper_prompt, mapper_system_prompt, get_unblur_prompt, unblur_system_prompt
from localcall import local_call


def get_dictionary_response(response):
    # parse the mapper model's response to a dictionary
    response_line = response.split("\n")
    flag = False
    ret = ""
    for line in response_line:
        if (line.find("{") != -1):
            flag = True
        ret += line
        if (line.find("}") != -1):
            break
    ret = ret.replace("\n", "").replace("\t", "").replace("\\", "")
    if flag:
        try:
            return json.loads(ret)
        except:
            print("Error in parsing the response")
    print("No dictionary found in the response")
    return {}


def get_redacted_text(instruction, data_str, local_model):

    prompt = get_redactor_prompt(data_str)
    response = local_call(prompt, system_prompt=redactor_system_prompt, local_model=local_model)
    response = "".join(response).strip('```').strip()
    if response.find("```") != -1:
        response = response.split("```")[0]
    return response


def get_mapping(instruction, data, redacted_data, local_model):
    prompt = get_mapper_prompt(data, redacted_data)
    response = local_call(prompt, system_prompt=mapper_system_prompt, local_model=local_model)
    response = "".join(response).strip('```').strip()
    response = get_dictionary_response(response)
    if (type(response) == dict):
        return response
    else:
        return {}


def get_unblur_response(remote_response, sensitive_mapping: dict, local_model, use_python=True):
    if use_python:
        ## simple python-based replacement
        # First make sure all the keys in the mappings don't have any special characters
        # apart from square brackets and underscore
        for key in sensitive_mapping.keys():
            new_key = re.sub(r'[^a-zA-Z0-9_\[\]]', '', key)
            if new_key != key:
                sensitive_mapping[new_key] = sensitive_mapping.pop(key)

        # Since the original text may have square brackets around the keys, we need to
        # replace them with the keys without the square brackets
        unblurred_response = re.sub(r'\[([a-zA-Z0-9_]+)\]', r'\1', remote_response)

        # Now replace the keys with the values
        for key, value in sensitive_mapping.items():
            unblurred_response = unblurred_response.replace(key, value)

        return unblurred_response

    else:
        ## Original version using model
        prompt = get_unblur_prompt(remote_response, sensitive_mapping)
        response = local_call(prompt, system_prompt=unblur_system_prompt, local_model=local_model)
        response = "".join(response).strip('```').strip()
        if (response.find("```") != -1):
            response = response.split("```")[0]
        return response
