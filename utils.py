import fitz  # PyMuPDF
import matplotlib.pyplot as plt
import streamlit as st

def extract_text_from_pdf(uploaded_file):
    if hasattr(uploaded_file, "read"):  # Streamlit uploaded file
        file_data = uploaded_file.read()
        doc = fitz.open(stream=file_data, filetype="pdf")
    else:  # Plain string path
        doc = fitz.open(uploaded_file)
    
    return " ".join([page.get_text() for page in doc])


def match_skills(resume_skills, jd_skills):
    matched = list(set(resume_skills).intersection(set(jd_skills)))
    missing = list(set(jd_skills) - set(resume_skills))
    return matched, missing

def draw_pie_chart(matched_count, missing_count):
    labels = ['Matched Skills', 'Missing Skills']
    values = [matched_count, missing_count]
    colors = ['#28a745', '#dc3545']
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    ax.axis('equal')
    st.pyplot(fig)
