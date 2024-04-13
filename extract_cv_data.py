import os
import re
import pandas as pd
from PyPDF2 import PdfReader
from flask import Flask, request, redirect, send_file
from werkzeug.utils import secure_filename
from io import BytesIO
from docx import Document

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'doc'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(pdf_bytes):
    text = ""
    reader = PdfReader(BytesIO(pdf_bytes))
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(docx_bytes):
    text = ""
    doc = Document(BytesIO(docx_bytes))
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text

def extract_text_from_text_file(txt_bytes):
    return txt_bytes.decode('utf-8')

def find_emails(text):
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return emails

def find_phone_numbers(text):
    phone_numbers = re.findall(r'\b(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})\b', text)
    formatted_numbers = ['{}{}{}{}'.format(num[0], num[1], num[2], num[3]) for num in phone_numbers]
    return formatted_numbers

def process_cv(file):
    filename, file_extension = os.path.splitext(file.filename)
    file_contents = file.read()
    file.seek(0)  # Reset file pointer to beginning for further processing

    try:
        if file_extension.lower() == '.pdf':
            text = extract_text_from_pdf(file_contents)
        elif file_extension.lower() == '.docx':
            text = extract_text_from_docx(file_contents)
        elif file_extension.lower() == '.txt':
            text = extract_text_from_text_file(file_contents)
        elif file_extension.lower() == '.doc':
              text = extract_text_from_text_file(file_contents)
        else:
            raise ValueError("Unsupported file format")

        emails = find_emails(text)
        phone_numbers = find_phone_numbers(text)

        data = {'Email': '; '.join(emails), 'Phone Number': '; '.join(phone_numbers), 'Text': text}

        df = pd.DataFrame([data])
        return df
    except Exception as e:
        app.logger.error(f"Error processing file {file.filename}: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_files = request.files.getlist('file')
        df_list = []
        for file in uploaded_files:
            if file and allowed_file(file.filename):
                df = process_cv(file)
                if df is not None:
                    df_list.append(df)
                else:
                    app.logger.warning(f"Skipping file {file.filename} due to processing error.")
        if df_list:
            combined_df = pd.concat(df_list, ignore_index=True)
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.xlsx')
            combined_df.to_excel(output_path, index=False)
            return send_file(output_path, as_attachment=True)
    return '''
    <!doctype html>
    <title>Upload new CV</title>
    <h1>Upload new CV</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file multiple>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
