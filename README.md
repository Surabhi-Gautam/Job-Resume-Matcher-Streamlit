Job Description and Resume Matcher
This application helps users rank resumes against a given job description using TF-IDF vectorisation and Cosine Similarity, supporting various document formats. It's designed as a practical AI/ML course project to demonstrate concepts in text processing and information retrieval.

Features
Intelligent Matching: Utilises TF-IDF (Term Frequency-Inverse Document Frequency) and Cosine Similarity to calculate relevance scores between job descriptions and resumes.

Multi-Format Support: Seamlessly accepts resume uploads in .txt, .pdf, and .docx formats, extracting text content for analysis.

Real-time Scoring: Provides immediate match scores and a ranked list of resumes, allowing for quick assessment.

User-Friendly Interface: Built with Streamlit, offering an intuitive web-based interface for easy interaction.

Detailed View: Users can expand each resume entry in the results to view its original extracted text content.

🛠️ Technologies Used
Python: The core programming language for the application logic.

Streamlit: For building the interactive and responsive web user interface.

Scikit-learn: Provides robust tools for TF-IDF vectorisation and Cosine Similarity calculations.

Pandas: Used for efficient data handling and structuring the match results for display.

PyPDF: A pure-Python PDF library used for extracting text content from .pdf documents.

Python-Docx: A library for creating and updating Microsoft Word .docx files, used here for text extraction.

Setup and Installation
To get this project up and running on your local machine, follow these steps:

Clone the repository:
First, open your terminal or command prompt and clone the project repository from GitHub:

git clone https://github.com/Surabhi-Gautam/Job-Resume-Matcher-Streamlit.git
cd Job-Resume-Matcher-Streamlit

Create and activate a virtual environment:
It's highly recommended to use a virtual environment to manage the project's dependencies and avoid conflicts with other Python projects on your system.

python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# For Windows, use: .venv\Scripts\activate

You'll know the virtual environment is active when (.venv) appears at the beginning of your terminal prompt.

Install the required Python packages:
With your virtual environment activated, install all the necessary libraries listed in requirements.txt:

pip install -r requirements.txt

Run the Streamlit application:
Once all packages are installed, you can launch the application:

streamlit run app.py

This command will open the Job Description Matcher application in your default web browser.

How to Use
Once the Streamlit application is running in your browser:

Enter Job Description: Paste the full job description text into the "Paste the job description here:" text area.

Upload Resumes: Use the "Upload resume files (.txt, .pdf, .docx)" section to upload one or more resume files from your computer. The application supports .txt, .pdf, and .docx formats.

Paste Resumes (Optional): Alternatively, for quick tests or if you prefer, you can paste resume text directly into the "Alternatively, paste resumes here..." text area. If pasting multiple resumes, ensure each is separated by ---RESUME-SEPARATOR---.

Calculate Scores: Click the "Calculate Match Scores" button.

View Results: The application will process the inputs and display a ranked list of resumes with their calculated match scores (as percentages).

Detailed Content: For each resume in the results, you can click on "View Original Resume Content" to see the full text extracted from that resume.

Contributing
Contributions are welcome! If you have suggestions for improvements, bug fixes, or new features, feel free to:

Fork the repository.

Create a new branch (git checkout -b feature/YourFeature).

Make your changes.

Commit your changes (git commit -m 'Add new feature').

Push to the branch (git push origin feature/YourFeature).

Open a Pull Request.

License
This project is open-sourced under the MIT License. See the LICENSE file (if applicable) for more details.