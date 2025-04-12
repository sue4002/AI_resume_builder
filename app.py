
import streamlit as st
from io import BytesIO
from PIL import Image
import pandas as pd
import plotly.express as px

# Title for the Resume Builder
st.title("AI Resume Builder with Profile Picture Upload")

# Sidebar for the User Input
st.sidebar.header("Personal Information")

# Name Input
name = st.sidebar.text_input("Full Name")
email = st.sidebar.text_input("Email")
phone = st.sidebar.text_input("Phone Number")
address = st.sidebar.text_area("Address")

# Resume Photo Upload
uploaded_file = st.sidebar.file_uploader("Upload Your Profile Picture", type=["png", "jpg", "jpeg"])

# Show Image if Uploaded
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.sidebar.image(image, caption="Uploaded Profile Picture", use_column_width=True)

# Education Details
st.sidebar.header("Education Details")
degree = st.sidebar.text_input("Degree")
institution = st.sidebar.text_input("Institution Name")
graduation_year = st.sidebar.number_input("Graduation Year", min_value=2000, max_value=2025)

# Skills Input
skills = st.sidebar.text_area("Skills (Comma Separated)")

# Experience Input
experience = st.sidebar.text_area("Previous Job Experience")

# Button to generate the Resume
if st.sidebar.button("Generate Resume"):
    st.subheader("Generated Resume")

    # Show Uploaded Profile Picture on the Resume
    if uploaded_file is not None:
        st.image(image, caption="Your Profile Picture", width=150)

    # Show the Resume Information
    st.write("*Name*:", name)
    st.write("*Email*:", email)
    st.write("*Phone*:", phone)
    st.write("*Address*:", address)

    # Show Education Details
    st.write("*Degree*:", degree)
    st.write("*Institution*:", institution)
    st.write("*Graduation Year*:", graduation_year)

    # Display Skills
    st.write("*Skills*:", skills)

    # Show Experience
    st.write("*Previous Experience*:", experience)

    # Add Some Basic Animation or Loading Spinners
    with st.spinner('Generating your resume...'):
        st.write("Resume is ready!")

    # Optional: Create a simple bar chart showing skills as categories (or any other data visualization)
    skill_list = skills.split(",")
    skills_df = pd.DataFrame({
        "Skills": skill_list,
        "Count": [1] * len(skill_list)  # Simple count for each skill
    })

    fig = px.bar(skills_df, x='Skills', y='Count', title="Skills Distribution")
    st.plotly_chart(fig)

    # Add some more interactive animations (e.g., Plotly animations)
    st.markdown("""
        <style>
        .stApp {
            animation: fadeIn 2s ease-in-out;
        }
        @keyframes fadeIn {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }
        </style>
>>>>>>> aa34b801cbdcc8db7ebdaf3be4f28720de3807c6
    """, unsafe_allow_html=True)