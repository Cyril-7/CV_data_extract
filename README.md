# CV Processing Tool

![image](https://github.com/Cyril-7/CV_data_extract/assets/129573220/da156ebb-0894-4128-89f2-e4bdd3ecdbb9)


## Overview
This is a Flask-based web application designed to process resumes or CVs (Curriculum Vitae) uploaded by users. The application extracts information such as email addresses and phone numbers from the CVs and generates an Excel file with the extracted data.

## Features
- Supports multiple file formats: PDF, DOCX, TXT, and DOC.
- Extracts email addresses and phone numbers from the uploaded CVs.
- Provides a simple web interface for users to upload CVs.
- Outputs the extracted information into an Excel file for easy access.

## Setup
1. **Dependencies**: Make sure you have Python installed on your system along with the required libraries listed in the `requirements.txt` file. You can install them using pip:
   ```
   pip install -r requirements.txt
   ```
2. **Run the Application**: Execute the `app.py` file to start the Flask server:
   ```
   python app.py
   ```
   The application will run locally on `http://127.0.0.1:5000/`.

## Usage
1. Access the application through a web browser.
2. Click on the "Upload new CV" button.
3. Select one or more CV files (PDF, DOCX, TXT, or DOC) from your local system.
4. Click on the "Upload" button to submit the files.
5. Wait for the processing to complete. The application will generate an Excel file containing the extracted information.
6. Download the Excel file from the provided link.

## File Structure
- `app.py`: Main Flask application file containing the server logic.
- `uploads/`: Directory to store uploaded files and generated output files.
- `README.md`: Documentation file providing information about the application.


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to customize this README with additional details or instructions specific to your project!
