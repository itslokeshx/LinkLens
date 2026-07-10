import os
import streamlit as st
from dotenv import load_dotenv
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_groq import ChatGroq

load_dotenv()

st.set_page_config(
    page_title="LinkLens",
    page_icon="🔗",
    layout="centered"
)

st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }
    
    div.stButton > button {
        background-color: transparent !important;
        color: inherit !important;
        border: 1px solid rgba(128, 128, 128, 0.3) !important;
        padding: 0.5rem 1.25rem !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
    }
    
    div.stButton > button:hover {
        border-color: rgba(128, 128, 128, 0.8) !important;
        background-color: rgba(128, 128, 128, 0.05) !important;
    }
    
    div.stButton > button:active {
        background-color: rgba(128, 128, 128, 0.1) !important;
    }
    
    div.stTextInput > div > div > input {
        border-radius: 6px !important;
        padding: 0.6rem 0.85rem !important;
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
        background-color: transparent !important;
        transition: all 0.2s ease !important;
        font-size: 0.95rem !important;
    }
    
    div.stTextInput > div > div > input:focus {
        border-color: rgba(128, 128, 128, 0.6) !important;
        box-shadow: none !important;
    }
    
    div[data-testid="stNotification"] {
        border-radius: 6px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="padding: 1.5rem 0 1rem 0;">
        <h1 style="font-size: 2rem; font-weight: 600; margin-bottom: 0.25rem; letter-spacing: -0.5px;">
            LinkLens
        </h1>
        <p style="color: #64748b; font-size: 0.95rem; margin-bottom: 1.5rem;">
            A minimal tool to summarize web pages.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("GROQ_API_KEY not found in .env")
    st.stop()

url = st.text_input(
    label="Website URL",
    placeholder="Enter URL to summarize...",
    label_visibility="collapsed"
)

summarize = st.button(
    "Summarize",
    use_container_width=True
)

if summarize:
    if not url:
        st.warning("Please enter a URL.")
        st.stop()

    with st.spinner("Processing..."):
        try:
            loader = UnstructuredURLLoader(
                urls=[url]
            )
            documents = loader.load()
            llm = ChatGroq(
                model="openai/gpt-oss-20b",
                api_key=groq_api_key
            )
            prompt = PromptTemplate(
                input_variables=["text"],
                template="""
You are an expert summarizer.

Summarize the following content in concise bullet points.

{text}
"""
            )
            chain = load_summarize_chain(
                llm=llm,
                chain_type="stuff",
                prompt=prompt
            )
            response = chain.invoke(
                {
                    "input_documents": documents
                }
            )
            
            summary_html = f"""
            <div style="border-top: 1px solid rgba(128, 128, 128, 0.2); margin-top: 2rem; padding-top: 1.5rem;">
                <h3 style="font-weight: 600; font-size: 1.1rem; margin-bottom: 0.75rem;">Summary</h3>
                <div style="font-size: 0.95rem; line-height: 1.6; color: inherit;">
                    {response["output_text"]}
                </div>
            </div>
            """
            st.markdown(summary_html, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(str(e))
