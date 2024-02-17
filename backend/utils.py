import json
import re
from ast import literal_eval
def clear_filter_response(response):
    response_line = response.split("\n")
    flag = False
    ret = ""
    for line in response_line:
        if(line.find("{") != -1):
            flag = True
        ret += line
        if(line.find("}") != -1):
            break
    if(flag):
        try:
            return json.loads(ret)
        except:
            print("Error in parsing the response")
    print("No dictionary found in the response")