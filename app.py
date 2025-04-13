import streamlit as st
from io import BytesIO
from PIL import Image
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import os

# Streamlit page setup
st.set_page_config(page_title="AI Resume Builder", layout="centered", initial_sidebar_state="expanded")

# --- Styling for Dark Theme & Input Fix ---
st.markdown("""
    <style>
        body, .stApp {
            background-color: #1e1e1e;
            color: white;
        }
        input, textarea {
            color: white !important;
            background-color: #333333 !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📝 AI Resume Builder ")

# --- Sidebar Inputs ---
st.sidebar.header("Enter your details")

name = st.sidebar.text_input("Full Name")
email = st.sidebar.text_input("Email")
phone = st.sidebar.text_input("Phone Number")
address = st.sidebar.text_area("Address")

uploaded_file = st.sidebar.file_uploader("Upload Your Profile Picture", type=["png", "jpg", "jpeg"])
image = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.sidebar.image(image, caption="Uploaded Image", use_container_width=True)

st.sidebar.subheader("Education")
degree = st.sidebar.text_input("Degree")
institution = st.sidebar.text_input("Institution Name")
graduation_year = st.sidebar.number_input("Graduation Year", min_value=2000, max_value=2035)

skills = st.sidebar.text_area("Skills (Comma Separated)")
experience = st.sidebar.text_area("Work Experience")

st.sidebar.subheader("Optional")
certifications = st.sidebar.text_area("Certifications (Optional)")
projects = st.sidebar.text_area("Projects (Optional)")

linkedin = st.sidebar.text_input("LinkedIn URL (Optional)")
github = st.sidebar.text_input("GitHub URL (Optional)")

# --- Generate Resume Button ---
if st.sidebar.button("Generate Resume"):
    st.success("✅ Resume Generated Below")

    # Create a PDF object
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # --- Header Layout ---
    if uploaded_file:
        img_path = "temp_profile.jpg"
        image.save(img_path)
        pdf.image(img_path, x=10, y=10, w=40)
        os.remove(img_path)

    pdf.set_xy(60, 10)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, name, ln=1)

    pdf.set_font("Arial", '', 12)
    pdf.set_x(60)
    pdf.cell(0, 8, f"Email: {email}", ln=1)
    pdf.set_x(60)
    pdf.cell(0, 8, f"Phone: {phone}", ln=1)
    pdf.set_x(60)
    pdf.multi_cell(0, 8, f"Address: {address}")

    # --- Section Divider ---
    def section_title(title):
        pdf.set_font("Arial", 'B', 14)
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(0, 10, title, ln=1, fill=True)

    def bordered_box(content_lines):
        pdf.set_font("Arial", size=12)
        start_y = pdf.get_y()
        start_x = 10
        box_width = 190
        line_height = 8
        height = line_height * len(content_lines)

        pdf.rect(start_x, start_y, box_width, height + 4)
        pdf.ln(2)
        for line in content_lines:
            pdf.cell(0, line_height, line, ln=1)

    pdf.ln(5)
    section_title("Education")
    bordered_box([f"{degree} from {institution} ({graduation_year})"])

    if certifications:
        pdf.ln(5)
        section_title("Certifications")
        bordered_box(certifications.strip().split('\n'))

    if projects:
        pdf.ln(5)
        section_title("Projects")
        bordered_box(projects.strip().split('\n'))

    if skills:
        pdf.ln(5)
        section_title("Skills")
        skill_list = [f"- {s.strip()}" for s in skills.split(',')]
        bordered_box(skill_list)

    if experience:
        pdf.ln(5)
        section_title("Work Experience")
        bordered_box(experience.strip().split('\n'))

    if linkedin or github:
        pdf.ln(5)
        section_title("Links")
        links = []
        if linkedin:
            links.append(f"LinkedIn: {linkedin}")
        if github:
            links.append(f"GitHub: {github}")
        bordered_box(links)

    pdf.set_y(-25)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 10, "Generated using AI Resume Builder", ln=1, align='C')

    # Output PDF
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    st.download_button(
        label="📥 Download Resume as PDF",
        data=pdf_output,
        file_name=f"{name.replace(' ', '_')}_Resume.pdf",
        mime="application/pdf"
    )

    # --- Web Preview ---
    st.subheader("📑 Resume Preview")
    if uploaded_file:
        st.image(image, caption="Your Profile Picture", width=150)

    st.write(f"*Name*: {name}")
    st.write(f"*Email*: {email}")
    st.write(f"*Phone*: {phone}")
    st.write(f"*Address*: {address}")
    st.write(f"*Degree*: {degree}")
    st.write(f"*Institution*: {institution}")
    st.write(f"*Graduation Year*: {graduation_year}")
    st.write(f"*Skills*: {skills}")
    st.write(f"*Work Experience*: {experience}")
    if certifications:
        st.write(f"*Certifications*: {certifications}")
    if projects:
        st.write(f"*Projects*: {projects}")
    if linkedin:
        st.markdown(f"[🔗 LinkedIn Profile]({linkedin})", unsafe_allow_html=True)
    if github:
        st.markdown(f"[🔗 GitHub Profile]({github})", unsafe_allow_html=True)

    if skills:
        st.subheader("📊 Skill Distribution")
        skill_df = pd.DataFrame({'Skills': [s.strip() for s in skills.split(',')], 'Count': 1})
        fig = px.bar(skill_df, x="Skills", y="Count", title="Skill Breakdown", color="Skills")
        st.plotly_chart(fig)