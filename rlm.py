'''import libraries'''
import re
import os
import textwrap
import xml.etree.ElementTree as ET
import openai
import google.generativeai as genai
import pyodbc
import json
import mysql.connector
from mysql.connector import Error
from IPython.display import Markdown
from datetime import datetime

def to_markdown(text):
  '''method to generate the markdown text'''
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def connect_to_vertexai():
     '''method to authorize the connection to VertexAI api'''
     genai.configure(api_key="")
     model = genai.GenerativeModel('gemini-1.5-flash')
     return model

def get_gemini_response(model, request):
     '''method to request content from VertexAI gemini LLM'''
     response = model.generate_content(request)
     return extract_sql_query(response.text)

def connect_to_openai():
    '''method to authorize the connection to OpenAI api'''
    openai.organization = ""
    openai.api_key = ""
    openai.Model.list()
    model_name = "gpt-3.5-turbo"
    return model_name

def get_gpt_response(model_input, instruction, request):
    '''method to request content from OpenAI gpt LLM'''
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
    '''method for replacing config key-matches in response text'''
    for match in match_replace:
            if str(match) !='{}':
                for key, value in match.items():
                    if key in code_input:
                        code_input=code_input.replace(key, value)
    return code_input

def get_config_match(match_input, match_replace):
    '''method to find the config keys from configuration'''
    matched=''
    for match in match_replace:
            if str(match) !='{}':
                for key, value in match.items():
                    if key == match_input:
                        matched=value
    return str(matched)

def read_reportxpress_config(tag_value, lang_input):
    '''method to read from reportxpress configuration files'''
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

def extract_sql_query(text):
  '''method to extract exact sql queries from the llm response'''
  text = text.strip('"')
  start_index = text.find('SELECT')
  sql_query = text[start_index:]
  sql_query = re.sub(r'\W+$', '', sql_query)
  return sql_query

def get_gpt_query(request):
    '''mathod to generate query content using openai gpt LLM model'''
    model = connect_to_openai()
    instructions=''
    reportquery = get_gpt_response(model, instructions, request)
    reportdata = reportquery
    return reportdata

def get_gemini_query(request):
    '''mathod to generate query content using vertexai gemini LLM model'''
    model = connect_to_vertexai()
    reportquery = get_gemini_response(model, request)
    return reportquery

def execute_query(query):
    '''method to connect with Azure Cloud SQL and execute the query on the application database to get the report data'''
    connection = mysql.connector.connect(
        host='elevatu.mysql.pythonanywhere-services.com',
        user='elevatu',
        password='',
        database='elevatu$bank_db'
        )

    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute(query)
        column_names = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(column_names, row)) for row in rows]
        report_data=[]
        for row in data:
            report_data.append(row)
        cursor.close()
        connection.close()
    else:
        report_data="Error"

    return report_data

def execute_query_azure(query):
    '''method to connect with Azure Cloud SQL and execute the query on the application database to get the report data'''
    server = 'tcp:elevateu-reportxpress.database.windows.net,1433'
    database = 'bank_db'
    username = 'elevateu'
    password = ''
    conn_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(query)
    column_names = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    data = [dict(zip(column_names, row)) for row in rows]
    report_data=[]
    for row in data:
        report_data.append(row)
    cursor.close()
    conn.close()
    return report_data

def extract_data(query):
    '''method to execute the query on application database and get the data extract'''
    report_data = execute_query(query)
    return report_data

def build_prompts(input):
    with open('bank_db_schema.json', 'r') as file:
        data = json.load(file)
    prompt_str = str(data) + ", Based on this schema, write a SQL query to: "
    prompt_str = prompt_str + input
    prompt_str = prompt_str + ", write only sql query. no any additional text"
    return prompt_str

def get_report_data(input):
    '''main maithod to be called from api end-point'''
    request_input = build_prompts(input)
    query = get_gemini_query(request_input)
    report_data = extract_data(query)
    return str(report_data)
