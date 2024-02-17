def Filter_prompt(user_prompt, file_prompt):
    return f"""please remove all sensitive data from the document below{user_prompt}{file_prompt}
and return in json format as {{"sensitive_data": , "filtered_data": }}. """

def Extract_prompt(response_prompt, sensitive_data):
    return f"""please fill the sensitive_data {sensitive_data} into {response_prompt} and return"""
