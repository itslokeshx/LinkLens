# 🔗 LinkLens

> AI-powered webpage summarization from a single URL.

LinkLens is a lightweight web application that extracts the main content from a webpage and generates a concise AI summary. Simply paste a URL, and LinkLens handles the reading and summarization for you.

---

## ✨ Features

- 🌐 Summarize any publicly accessible webpage
- 🤖 AI-powered summaries using Groq
- ⚡ Simple and responsive Streamlit interface
- 📄 Clean and easy-to-read output
- 🔒 API key managed securely through environment variables

---

## 🏗️ Tech Stack

- Python
- Streamlit
- LangChain
- Groq
- Unstructured
- BeautifulSoup

---

## 🚀 Getting Started

### Clone the repository

```bash
git clone https://github.com/itslokeshx/LinkLens.git
cd LinkLens
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file from the example.

```bash
cp .env.example .env
```

Add your Groq API key.

```env
GROQ_API_KEY=your_groq_api_key
```

### Run the application

```bash
streamlit run app.py
```

---

## 💡 How It Works

```text
URL
 │
 ▼
UnstructuredURLLoader
 │
 ▼
Extract Webpage Content
 │
 ▼
Prompt Template
 │
 ▼
Groq LLM
 │
 ▼
AI Summary
```

---

## 📂 Project Structure

```text
LinkLens/
├── app.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## 📸 Preview

Coming soon.

---

## 📄 License

This project is licensed under the MIT License.
