import os
import re
import requests
from bs4 import BeautifulSoup
import streamlit as st
from dotenv import load_dotenv
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import UnstructuredURLLoader, YoutubeLoader
from langchain_groq import ChatGroq

load_dotenv()

def get_page_title(url):
    try:
        if "youtube.com" in url or "youtu.be" in url:
            oembed_url = f"https://www.youtube.com/oembed?url={url}&format=json"
            res = requests.get(oembed_url, timeout=5)
            if res.status_code == 200:
                title = res.json().get("title")
                if title:
                    return title
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }
        res = requests.get(url, headers=headers, timeout=5)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        title_tag = soup.find("title")
        if title_tag:
            title = title_tag.text.strip()
            if " - YouTube" in title:
                title = title.replace(" - YouTube", "")
            return title
    except Exception:
        pass
    return None

def parse_markdown_sections(text):
    pattern = r"^((?:#{2,4}\s+.*|\*\*.*?\*\*:?))$"
    parts = re.split(pattern, text, flags=re.MULTILINE)
    sections = []
    first_part = parts[0].strip()
    if first_part:
        sections.append(("", first_part))
    for i in range(1, len(parts), 2):
        header = parts[i].lstrip("#").strip("*").strip(":").strip()
        content = parts[i+1].strip() if i+1 < len(parts) else ""
        sections.append((header, content))
    return sections


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

    title = None
    with st.spinner("Fetching page details..."):
        title = get_page_title(url)

    spinner_text = f"Summarizing: {title}..." if title else "Summarizing..."
    with st.spinner(spinner_text):
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

Then, write a clean, structured summary using concise bullet points. Organize the bullet points under clear, descriptive section headers starting with '###' (for example: ### Key Themes, ### Main Takeaways, ### Practical Tips).

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
            
            if title:
                st.markdown(
                    f"""
                    <div style="
                        border: 1px solid rgba(128, 128, 128, 0.2);
                        padding: 1.25rem;
                        border-radius: 8px;
                        margin-top: 1rem;
                        margin-bottom: 1.5rem;
                        background-color: rgba(128, 128, 128, 0.02);
                    ">
                        <span style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: #64748b; font-weight: 600;">
                            Summary of
                        </span>
                        <h2 style="margin: 0.25rem 0 0.5rem 0; font-size: 1.35rem; font-weight: 600; line-height: 1.3; border: none; padding: 0;">
                            {title}
                        </h2>
                        <a href="{url}" target="_blank" style="font-size: 0.8rem; color: #3b82f6; text-decoration: none; word-break: break-all; display: inline-flex; align-items: center; gap: 4px;">
                            🔗 View Source
                        </a>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            if thinking:
                st.write("")
                with st.expander("Thinking Process", expanded=False):
                    st.markdown(thinking)
            
            st.write("")
            
            sections = parse_markdown_sections(summary)
            valid_sections = [s for s in sections if s[0]]
            
            if valid_sections:
                tab_titles = ["Full Summary"] + [s[0] for s in valid_sections]
                tabs = st.tabs(tab_titles)
                
                with tabs[0]:
                    st.write("")
                    st.markdown(summary)
                
                for tab, (header, content) in zip(tabs[1:], valid_sections):
                    with tab:
                        st.write("")
                        st.markdown(content)
            else:
                st.markdown(summary)
            
        except Exception as e:
            st.error(str(e))
