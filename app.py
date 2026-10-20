import streamlit as st

st.title("AI Resume Matcher")

st.write("Welcome to the Resume Matcher application!")

resume = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Enter Job Description"
)

if st.button("Analyze Resume"):
    if resume and job_description.strip():
        st.success("Resume uploaded successfully!")
        st.info("Resume matching analysis will be added here.")
    else:
        st.warning("Please upload a resume and enter a job description.")
