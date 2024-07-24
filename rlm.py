'''import libraries'''
import re
import os
import ast
import xml.etree.ElementTree as ET
import spacy
import openai

#load language library
nlp = spacy.load('en_core_web_sm')

def connect_to_openai():
    '''authorise the connection to OpenAI api'''
    openai.organization = ""
    openai.api_key = ""
    openai.Model.list()
    model_name = "gpt-3.5-turbo"
    return model_name

def get_response(model_input, instruction, request):
    '''method to request suggestion from OpenAI API'''
    response = openai.ChatCompletion.create(
        model=model_input,
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": request},
        ],
        temperature=0,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response['choices'][0]['message']['content']

def reportxpress_finetuning(code_input, match_replace):
    '''replacing config key-matches in response text'''
    for match in match_replace:
            if str(match) !='{}':
                for key, value in match.items():
                    if key in code_input:
                        code_input=code_input.replace(key, value)
    return code_input

def get_config_match(match_input, match_replace):
    '''find the config keys from configuration'''
    matched=''
    for match in match_replace:
            if str(match) !='{}':
                for key, value in match.items():
                    if key == match_input:
                        matched=value
    return str(matched)

def read_reportxpress_config(tag_value, lang_input):
    '''read from reportxpress configuration files'''
    current_dir = os.path.dirname(__file__)
    tree = ET.parse(current_dir + "/reportxpress-config.xml")
    root = tree.getroot()
    match_replace_list=[{}]
    for child in root:
        match_dict=child.attrib
        match = match_dict.get(tag_value)
        replace=child.text
        match_replace={match: replace}
        match_replace_list.append(match_replace)
    return match_replace_list


def generate_report(request):
    '''main mathod to trigger the report generation processing'''
    model = connect_to_openai()
    instructions=''
    reportquery = get_response(model, instructions, request)
    reportdata = reportquery
    return reportdata
