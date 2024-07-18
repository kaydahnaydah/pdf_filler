from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import pandas as pd
import PyPDF2
from app import app
from app.forms import UploadForm

# Directory to store uploaded files
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'csv', 'txt', 'xlsx'}

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for home page
@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        # Handle file upload
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        
        file = request.files['file']

        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Determine file type and process accordingly
            if filename.endswith('.pdf'):
                # Process PDF
                process_pdf(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            elif filename.endswith('.csv') or filename.endswith('.txt') or filename.endswith('.xlsx'):
                # Process CSV, TXT, Excel
                process_data_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                flash('Unsupported file type', 'error')
            
            flash('File uploaded successfully', 'success')
            return redirect(url_for('index'))

    return render_template('index.html', form=form)

# Function to process uploaded PDF file
def process_pdf(filepath):
    # Implement PDF processing logic using PyPDF2
    # For simplicity, just printing fields for demonstration
    pdf_file = open(filepath, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    num_pages = pdf_reader.numPages
    fields = {}

    for page_num in range(num_pages):
        page = pdf_reader.getPage(page_num)
        fields.update(page.extract_text())

    pdf_file.close()
    print(fields)

# Function to process uploaded data file (CSV, TXT, Excel)
def process_data_file(filepath):
    # Implement data processing logic using pandas
    # For simplicity, just printing data for demonstration
    if filepath.endswith('.csv'):
        data = pd.read_csv(filepath)
    elif filepath.endswith('.txt'):
        data = pd.read_csv(filepath, delimiter='\t')
    elif filepath.endswith('.xlsx'):
        data = pd.read_excel(filepath)
    else:
        return

    print(data.head())

# Route for about page
@app.route('/about')
def about():
    return render_template('about.html')

# Other routes (products, pricing, terms) can be similarly defined

if __name__ == '__main__':
    app.run(debug=True)