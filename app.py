import os
import re
import streamlit as st
from dotenv import load_dotenv
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import UnstructuredURLLoader, YoutubeLoader
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
        padding: 0.55rem 1.25rem !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
        height: 42px !important;
        width: 100% !important;
        line-height: 1.2 !important;
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
        padding: 0.55rem 0.85rem !important;
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
        background-color: transparent !important;
        transition: all 0.2s ease !important;
        font-size: 0.95rem !important;
        height: 42px !important;
    }
    
    div.stTextInput > div > div > input:focus {
        border-color: rgba(128, 128, 128, 0.6) !important;
        box-shadow: none !important;
    }
    
    div[data-testid="stNotification"] {
        border-radius: 6px !important;
    }
    
    div[data-testid="stExpander"] {
        border-radius: 6px !important;
        border: 1px solid rgba(128, 128, 128, 0.15) !important;
        background-color: transparent !important;
        box-shadow: none !important;
        margin-top: 1rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="padding: 1rem 0 1.5rem 0;">
        <h1 style="font-size: 1.75rem; font-weight: 600; margin-bottom: 0.15rem; letter-spacing: -0.3px;">
            LinkLens
        </h1>
        <p style="color: #64748b; font-size: 0.9rem; margin: 0;">
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

col1, col2 = st.columns([4, 1])

with col1:
    url = st.text_input(
        label="Website URL",
        placeholder="Enter URL to summarize...",
        label_visibility="collapsed"
    )

with col2:
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
            if "youtube.com" in url or "youtu.be" in url:
                loader = YoutubeLoader.from_youtube_url(
                    url,
                    add_video_info=False
                )
            else:
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

Analyze the text and organize your thoughts. First, write your analysis of the document structure, key themes, and main takeaways inside <thinking>...</thinking> XML tags.

Then, write a clean, structured summary using concise bullet points. Organize the bullet points under clear, bold section headers where appropriate.

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
            
            output_text = response.get("output_text", "")
            thinking = ""
            summary = output_text
            
            thinking_match = re.search(r"<thinking>(.*?)</thinking>", output_text, re.DOTALL)
            if thinking_match:
                thinking = thinking_match.group(1).strip()
                summary = re.sub(r"<thinking>.*?</thinking>", "", output_text, flags=re.DOTALL).strip()
            
            if thinking:
                st.write("")
                with st.expander("Thinking Process", expanded=False):
                    st.markdown(thinking)
            
            st.write("")
            st.markdown(summary)
            
        except Exception as e:
            st.error(str(e))
