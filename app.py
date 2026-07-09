
import os

from dotenv import load_dotenv
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY")
)

loader = UnstructuredURLLoader(
    urls=[
        "https://python.langchain.com/docs/introduction/"
    ]
)

documents = loader.load()

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

print(response["output_text"])
