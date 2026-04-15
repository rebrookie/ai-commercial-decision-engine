import os
import streamlit as st
from openai import OpenAI

def get_openai_client():
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except Exception:
        api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set")

    return OpenAI(api_key=api_key)