from pdfminer.high_level import extract_text
from utils import get_redacted_text, get_mapping, get_unblur_response
from remotecall import remote_call

import textwrap

Filter_result = {}
Sensitive_mapping = {}


def user_input(instruction="",
               data_str="",
               local_model="mistralai/Mixtral-8x7B-Instruct-v0.1",
               file_path=""):
    if (data_str == "" and file_path == ""):
        return "I see that you have not provided any data"
    return instruction, blur_data(instruction, data_str, local_model, file_path)


def process_request(instruction="",
                    blurred_data="",
                    local_model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                    remote_model="gpt-3.5-turbo"):
    remote_response = SendToRemote(instruction, blurred_data, remote_model)
    global Sensitive_mapping
    unblurred_response = UnblurResponse(remote_response, Sensitive_mapping, local_model)
    return remote_response, unblurred_response


def reblur_data(instruction="",
                data_str="",
                blurred_data="",
                local_model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                file_path=""):
    return blur_data(instruction, data_str, local_model, file_path)


def blur_data(instruction, data_str, local_model, file_path):
    file_data = ""
    if (file_path != None):
        if (file_path.endswith(".pdf")):
            file_data = extract_text(file_path)
        if (file_data.endswith(".txt")):
            file_data = extract_text(file_path)
    data = data_str + file_data
    redacted_data = get_redacted_text(instruction, data, local_model)
    mapping = get_mapping(instruction, data, redacted_data, local_model)
    global Sensitive_mapping
    Sensitive_mapping = mapping
    return redacted_data


def SendToRemote(instruction, blurred_data, remote_model):
    prompt = textwrap.dedent(f"""\
        Instruction: "{instruction}"
        Data: "{blurred_data}"
    """)
    response = remote_call(prompt, remote_model)
    return response


def UnblurResponse(remote_response="",
                   mapping={},
                   local_model="mistralai/Mixtral-8x7B-Instruct-v0.1"):
    response = get_unblur_response(remote_response, mapping, local_model)
    return response


if __name__ == '__main__':
    instructon = "can you help me refine the email"
    data = """Dear Sam Altman,

I am excited to submit my application for the CEO position at OpenAI. As a mid-level professional with 30 years of experience in Artificial Intelligence, I am confident that my skills and experience make me a strong candidate for the role.

In my current position at Deepmind, I have honed my skills in Artificial Int, which I believe would be a valuable asset to your team. I am particularly drawn to OpenAI's reputation for , and I am eager to contribute my expertise to help achieve the company's goals."""
    print("\n===data===")
    print(data)
    output = user_input(instruction="", data_str=data)
    print("\n===output===")
    print(output)
    print("\n===Sensitive_mapping===")
    print(Sensitive_mapping)
    raw_output, unblurred_response = process_request(instruction=instructon, blurred_data=output)
    print("\n===raw_output===")
    print(raw_output)
    print("\n===unblurred_response===")
    print(unblurred_response)
    #print(output)
