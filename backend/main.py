from flask import Flask, jsonify, request
from prompts import Filter_prompt, Extract_prompt
from apicall import get_public_response
from localcall import get_local_response
app = Flask(__name__)

#Global_result:
Filter_result = None
Sensitive_data = None
# A simple route that returns a JSON response
@app.route('/filter')
def filter():
    name = request.args.get('query', None)
    return f'Hello, {name}!'

@app.route('/pdf')
def get_pdf():
    # Assuming the PDF is in the 'files' directory under the root of your Flask app
    directory = "./files"
    filename = "example.pdf"
    return send_from_directory(directory, filename)

@app.route('/getanswer')
def getanswer():
    name = request.args.get('answer', 'Guest')
    return f'Hello, {name}!'

if __name__ == '__main__':
    app.run(port=5000, debug=True)