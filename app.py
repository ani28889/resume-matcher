import streamlit as st
from pypdf import PdfReader
import re

st.set_page_config(
    page_title="AI Resume Matcher",
    page_icon="📄",
    layout="centered"
)

st.title("📄 AI Resume Matcher")
st.write(
    "Upload your resume and compare it with a job description."
)

resume_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Enter Job Description",
    height=220,
    placeholder="Paste the job description here..."
)

# Extract text from PDF
def extract_resume_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


# Find skills mentioned in text
def find_skills(text):
    skills = [
        "python",
        "java",
        "c++",
        "machine learning",
        "artificial intelligence",
        "data analysis",
        "sql",
        "html",
        "css",
        "javascript",
        "streamlit",
        "github",
        "communication",
        "problem-solving",
        "teamwork",
        "deep learning",
        "pandas",
        "numpy",
        "excel",
        "power bi"
    ]

    text = text.lower()
    found = []

    for skill in skills:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):
            found.append(skill.title())

    return found


if st.button("Analyze Resume"):
    if resume_file is None:
        st.warning("Please upload your resume PDF.")

    elif not job_description.strip():
        st.warning("Please enter a job description.")

    else:
        try:
            with st.spinner("Analyzing your resume..."):

                resume_text = extract_resume_text(resume_file)

                if not resume_text.strip():
                    st.error(
                        "No readable text found in this PDF. "
                        "Please upload a text-based PDF."
                    )

                else:
                    resume_skills = find_skills(resume_text)
                    job_skills = find_skills(job_description)

                    if not job_skills:
                        st.warning(
                            "No supported skills were found in the "
                            "job description. Try adding skills such "
                            "as Python, SQL, or Machine Learning."
                        )

                    else:
                        matched = [
                            skill for skill in job_skills
                            if skill in resume_skills
                        ]

                        missing = [
                            skill for skill in job_skills
                            if skill not in resume_skills
                        ]

                        score = round(
                            len(matched) / len(job_skills) * 100
                        )

                        st.success("Resume analysis completed!")

                        st.subheader("📊 Matching Results")

                        st.metric(
                            "Skill Match Percentage",
                            f"{score}%"
                        )

                        st.progress(score / 100)

                        st.subheader("✅ Matching Skills")

                        if matched:
                            st.write(", ".join(matched))
                        else:
                            st.write(
                                "No matching skills found."
                            )

                        st.subheader("💡 Skills to Improve")

                        if missing:
                            st.write(", ".join(missing))
                        else:
                            st.write(
                                "All detected job skills matched!"
                            )

                        st.subheader("📋 Summary")

                        st.write(
                            f"Skills found in resume: "
                            f"{len(resume_skills)}"
                        )

                        st.write(
                            f"Skills requested by job: "
                            f"{len(job_skills)}"
                        )

                        st.caption(
                            "This score measures keyword skill overlap. "
                            "It is not a complete AI assessment of "
                            "experience, qualifications, or suitability."
                        )

        except Exception as error:
            st.error(
                "Could not analyze the PDF. "
                "Please upload a valid PDF and try again."
            )
            st.caption(str(error))
