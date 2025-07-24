import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import re
import io

# Libraries for PDF and DOCX
import pypdf # For reading PDF files
from docx import Document # For reading DOCX files

# --- 1. Text Preprocessing Function ---
def preprocess_text(text):
    """
    Cleans and preprocesses text by:
    - Converting to lowercase
    - Removing punctuation
    - Removing extra whitespace
    """
    text = text.lower() # Convert to lowercase
    text = re.sub(r'[^\w\s]', '', text) # Remove punctuation (keeps letters, numbers, whitespace)
    text = re.sub(r'\s+', ' ', text).strip() # Replace multiple spaces with single space and strip
    return text

# --- Helper Functions for File Content Extraction ---
def extract_text_from_pdf(file_bytes):
    """
    Extracts text from a PDF file.
    """
    text = ""
    try:
        # Use io.BytesIO to treat bytes as a file
        pdf_file = io.BytesIO(file_bytes)
        reader = pypdf.PdfReader(pdf_file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text() or "" # Add page text, handle None
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return None
    return text

def extract_text_from_docx(file_bytes):
    """
    Extracts text from a DOCX file.
    """
    text = ""
    try:
        # Use io.BytesIO to treat bytes as a file
        document = Document(io.BytesIO(file_bytes))
        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        st.error(f"Error reading DOCX file: {e}")
        return None
    return text

# --- 2. Streamlit Application Setup ---
st.set_page_config(layout="wide", page_title="Job-Resume Matcher")

st.title("📄 Job Description and Resume Matcher")
st.markdown("""
    This application helps you rank resumes against a given job description
    using TF-IDF vectorization and Cosine Similarity.
""")

# --- Input Section ---
st.header("1. Enter Job Description")
job_description_input = st.text_area(
    "Paste the job description here:",
    height=200,
    placeholder="e.g., We are looking for a highly motivated Data Scientist with experience in Python, Machine Learning, and SQL..."
)

st.header("2. Upload Resumes (or Paste Text)")

# Option to upload files - now accepts txt, pdf, docx
uploaded_files = st.file_uploader(
    "Upload resume files (.txt, .pdf, .docx). You can upload multiple files.",
    type=["txt", "pdf", "docx"], # Added pdf and docx
    accept_multiple_files=True
)

# Option to paste text (for backward compatibility or quick tests)
resumes_text_input = st.text_area(
    "Alternatively, paste resumes here (each separated by `---RESUME-SEPARATOR---`):",
    height=200,
    placeholder="""
    Resume 1: John Doe - Experienced Software Engineer with skills in Python, Java, AWS.
    ---RESUME-SEPARATOR---
    Resume 2: Jane Smith - Data Analyst with strong SQL, Excel, and some Python skills.
    """
)


# --- Processing Button ---
if st.button("Calculate Match Scores"):
    resume_list = []
    resume_names = [] # To store original file names or "Pasted Resume X"

    # Process uploaded files first
    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_name = uploaded_file.name
            file_extension = file_name.split('.')[-1].lower()
            resume_content = None

            if file_extension == "txt":
                string_io = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
                resume_content = string_io.read()
            elif file_extension == "pdf":
                resume_content = extract_text_from_pdf(uploaded_file.getvalue())
            elif file_extension == "docx":
                resume_content = extract_text_from_docx(uploaded_file.getvalue())
            else:
                st.warning(f"Unsupported file type for {file_name}: .{file_extension}. Skipping.")
                continue # Skip to next file

            if resume_content and resume_content.strip(): # Add only if content is successfully extracted and not empty
                resume_list.append(resume_content)
                resume_names.append(file_name)
            elif resume_content is None: # Indicates an error during extraction
                st.warning(f"Could not extract text from {file_name}. It might be corrupted or empty.")
        st.success(f"Successfully loaded {len(resume_list)} resume(s) from uploaded files.")

    # Process pasted text if files are not uploaded or if text is also provided
    if resumes_text_input.strip():
        pasted_resumes = [res.strip() for res in resumes_text_input.split("---RESUME-SEPARATOR---") if res.strip()]
        if pasted_resumes:
            resume_list.extend(pasted_resumes)
            # Assign generic names for pasted resumes
            for i in range(len(pasted_resumes)):
                resume_names.append(f"Pasted Resume {len(uploaded_files) + i + 1}")
            st.success(f"Successfully loaded {len(pasted_resumes)} resume(s) from pasted text.")

    if not job_description_input:
        st.error("Please enter a job description to proceed.")
    elif not resume_list:
        st.error("Please upload at least one resume file or paste resume text to proceed.")
    else:
        st.subheader("Processing...")

        # Preprocess all text
        processed_job_description = preprocess_text(job_description_input)
        processed_resumes = [preprocess_text(res) for res in resume_list]

        # Combine all text for TF-IDF vectorizer to learn the vocabulary
        corpus = [processed_job_description] + processed_resumes

        # --- 3. TF-IDF Vectorization ---
        vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
        tfidf_matrix = vectorizer.fit_transform(corpus)

        # Separate the TF-IDF vectors for job description and resumes
        job_desc_vector = tfidf_matrix[0:1] # First row is job description
        resume_vectors = tfidf_matrix[1:]   # Remaining rows are resumes

        # --- 4. Cosine Similarity Calculation ---
        similarity_scores = cosine_similarity(job_desc_vector, resume_vectors)[0]

        # --- 5. Ranking and Display Results ---
        results = []
        for i, score in enumerate(similarity_scores):
            results.append({
                "Resume ID": resume_names[i], # Use the stored name
                "Original Resume Text": resume_list[i],
                "Match Score": score * 100 # Convert to percentage
            })

        # Create a Pandas DataFrame for easy sorting and display
        results_df = pd.DataFrame(results)

        # Sort by Match Score in descending order
        results_df = results_df.sort_values(by="Match Score", ascending=False).reset_index(drop=True)

        st.header("3. Match Results")
        st.success("Matching complete! Here are the ranked resumes:")

        st.dataframe(results_df[['Resume ID', 'Match Score']].style.format({"Match Score": "{:.2f}%"}))

        st.markdown("---")
        st.subheader("Detailed Resume Content and Scores")
        for index, row in results_df.iterrows():
            st.markdown(f"**{row['Resume ID']}** (Match Score: **{row['Match Score']:.2f}%**)")
            with st.expander("View Original Resume Content"):
                st.text(row['Original Resume Text'])
            st.markdown("---")
