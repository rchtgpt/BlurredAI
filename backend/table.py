import pandas as pd
import re

def get_redacted_csv(data_str = "", file_path = "", local_model = ""):
    data = pd.read_csv(file_path)
    data.columns = [col.lower() for col in data.columns]
    for column in data.columns:
        if data[column].dtype == object:  # Checking for string columns
            data[column] = data[column].str.lower()
    
    i = 0
    mapping = {}
    for col in data.columns:
        mapping[col] = "[column{}]".format(i)
        i+=1
    changed_columns = []
    for column in data.columns:
        print(data[column].dtype, data[column].dtype == 'object')
        if data[column].dtype == 'object':
            changed_columns.append(column)
    for it, row in data.iterrows():
        for column in changed_columns:
            mapping[row[column]] = "[{}_{}]".format(mapping[column], it)
    column_mapping = {}
    for col in data.columns:
        if col in mapping:
            column_mapping[col] = mapping[col]
        else:
            column_mapping[col] = col
    data.replace(mapping, inplace=True)
    data.rename(columns=column_mapping, inplace=True)
    print(mapping)
    return data.to_string(), mapping

def get_response_csv(response, Sensitive_mapping, local_model):
    response = re.sub(r'\[([a-zA-Z0-9_]+)\]', r'\1', response)
    Sensitive_mapping = sorted(Sensitive_mapping.items(), key=lambda item: len(item[1]), reverse=True)
    for key,value in Sensitive_mapping:
        value = re.sub(r'\[([a-zA-Z0-9_]+)\]', r'\1', value)
        response = response.replace(value, key)
    return response