from pdfminer.high_level import extract_text
from utils import get_redacted_text, get_mapping, get_unblur_response
from remotecall import remote_call

Filter_result = {}
Sensitive_mapping = {}

def user_input(instruction = "", data_str = "", local_model = "mistralai/Mixtral-8x7B-Instruct-v0.1", file_path = ""):
    if(data_str == "" and file_path == ""):
        return "I see that you have not provided any data"
    return blur_data(instruction, data_str, local_model, file_path)

def process_request(instruction = "", blurred_data = "", local_model = "mistralai/Mixtral-8x7B-Instruct-v0.1" , remote_model = "gpt-3.5-turbo"):
    remote_response = SendToRemote(instruction, blurred_data, remote_model)
    global Sensitive_mapping
    unblurred_response = UnblurResponse(remote_response, Sensitive_mapping, local_model)
    return remote_response, unblurred_response

def reblur_data(instruction = "", data_str = "", blurred_data = "", local_model = "mistralai/Mixtral-8x7B-Instruct-v0.1", file_path = ""):
	return ""
 
def blur_data(instruction, data_str  , local_model, file_path):
    file_data = ""
    if(file_path != None):
        if(file_path.endswith(".pdf")):
            file_data = extract_text(file_path)
        if(file_data.endswith(".txt")):
            file_data = extract_text(file_path)
    data = data_str + file_data
    redacted_data = get_redacted_text(instruction, data, local_model)
    mapping = get_mapping(instruction, data, redacted_data, local_model)
    global Sensitive_mapping
    Sensitive_mapping = mapping
    return redacted_data

def SendToRemote(instruction, blurred_data, remote_model):
    data = instruction + "\n" + blurred_data
    response = remote_call(data, remote_model)
    return response

def UnblurResponse(remote_response = "", mapping = {}, local_model = "mistralai/Mixtral-8x7B-Instruct-v0.1"):
    response = get_unblur_response(remote_response, mapping, local_model)
    return response

def RedoBlurring(user_prompt = "", file_path = "", blurred_input = "", local_model = "mistralai/Mixtral-8x7B-Instruct-v0.1"):
    file_prompt = ""
    if(file_path != None):
        if(file_path.endswith(".pdf")):
            file_prompt = extract_text(file_path)
    redo_prompt = ""
    redo_result = ""
    return redo_result

if __name__ == '__main__':
    data = """Dear Sam Altman,

I am excited to submit my application for the CEO position at OpenAI. As a mid-level professional with 30 years of experience in Artificial Intelligence, I am confident that my skills and experience make me a strong candidate for the role.

In my current position at Deepmind, I have honed my skills in Artificial Int, which I believe would be a valuable asset to your team. I am particularly drawn to OpenAI's reputation for , and I am eager to contribute my expertise to help achieve the company's goals."""
    output = user_input(instruction = "", data_str =data)
    print(output)
    print(Sensitive_mapping)
    process_output = process_request(instruction = "help me refine the email", blurred_data = output)
    #print(output)
   # app.run(port=5000, debug=True)