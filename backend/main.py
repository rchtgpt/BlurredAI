from flask import Flask, jsonify, request
from prompts import Filter_prompt, Extract_prompt
from apicall import get_public_response
from localcall import get_local_response
from pdfminer.high_level import extract_text
from utils import clear_filter_response
app = Flask(__name__)

#Global_result:
Filter_result = None
Sensitive_data = None
# A simple route that returns a JSON response
@app.route('/blur_input')
def BlurInput():
    user_prompt = request.args.get('prompt', "")
    file_path = request.args.get('file_path', None)
    local_model = request.args.get('local_model', "mistralai/Mixtral-8x7B-Instruct-v0.1")
    file_prompt = ""
    if(file_path != None):
        if(file_path.endswith(".pdf")):
            file_prompt = extract_text(file_path)
    filter_prompt = Filter_prompt(user_prompt, file_prompt)
    response = get_local_response(local_model, filter_prompt)
    response_dict = clear_filter_response(response)
    Sensitive_data = response_dict["sensitive_data"]
    Filter_result = response_dict["filtered_data"]
    return response_dict["filtered_data"]

@app.route('/send_to_remote')
def SendToRemote():
    blurred_input = request.args.get('blurred_input', "")
    remote_mode = request.args.get('remote_model', "GPT-3.5-turbo")
    response = get_public_response(remote_mode, blurred_input)
    return response

@app.route('/redo_blurring')
def RedoBlurring():
    user_prompt = request.args.get('prompt', "")
    file_path = request.args.get('file_path', None)
    blurred_input = request.args.get('blurred_input', "")
    local_model = request.args.get('local_model', "mistralai/Mixtral-8x7B-Instruct-v0.1")
    file_prompt = ""
    if(file_path != None):
        if(file_path.endswith(".pdf")):
            file_prompt = extract_text(file_path)
    redo_prompt = ""
    redo_result = ""
    return redo_result

@app.route('/unblur_response')
def UnblurResponse():
    remote_response = request.args.get('remote_response', "")
    local_model = request.args.get('local_model', "mistralai/Mixtral-8x7B-Instruct-v0.1")
    unblurprompt = Extract_prompt(remote_response, Sensitive_data, Filter_result)
    response = get_local_response(local_model, unblurprompt)
    return response

if __name__ == '__main__':
    app.run(port=5000, debug=True)