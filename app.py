import os

from dotenv import load_dotenv
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_groq import ChatGroq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=GROQ_API_KEY
)

url = input("Enter URL: ")

loader = UnstructuredURLLoader(
    urls=[url]
)

documents = loader.load()

prompt = PromptTemplate(
    input_variables=["text"],
    template="""
You are an expert summarizer.

Summarize the following content in clear and concise bullet points.

{text}
"""
)

chain = load_summarize_chain(
    llm=llm,
    chain_type="stuff",
    prompt=prompt
)

summary = chain.invoke(
    {
        "input_documents": documents
    }
)

print("\nSummary\n")
print(summary["output_text"])
