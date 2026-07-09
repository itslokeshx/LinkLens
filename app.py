import os

import streamlit as st
from dotenv import load_dotenv
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_groq import ChatGroq

load_dotenv()

st.set_page_config(
    page_title="LinkLens",
    page_icon="🔗",
    layout="centered"
)

st.title("🔗 LinkLens")
st.caption("Summarize any webpage using AI")

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("GROQ_API_KEY not found in .env")
    st.stop()

url = st.text_input(
    "Website URL",
    placeholder="https://example.com"
)

summarize = st.button(
    "Summarize",
    use_container_width=True
)

if summarize:
    if not url:
        st.warning("Please enter a URL.")
        st.stop()

    with st.spinner("Reading webpage..."):
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

            st.subheader("Summary")
            st.markdown(response["output_text"])

        except Exception as e:
            st.error(str(e))
