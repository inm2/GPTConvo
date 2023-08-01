import openai
import streamlit as st
from dotenv import dotenv_values
import os
from csv_prompt import *

# Sidebar needs to have the following options:
# 1. CSV
# 2. PDF

# Get OpenAI credentials
config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]

with st.sidebar:
    uploaded_file = st.file_uploader("Choose a file (CSV or PDF)", accept_multiple_files=False)
    clear_button = st.button('Clear', on_click = reset_everything())

if uploaded_file is not None:
    file_extension = os.path.splitext(uploaded_file.name)[1]
    print(file_extension)

    if file_extension == (".csv"):
        # selection = st.radio("Choose a prompting technique", ('One-Shot', 'Few-Shot'))
        csv_reader(uploaded_file)

    if file_extension == ".pdf":
        pass
        # Initialize session state variable

        # Call pdf reader
