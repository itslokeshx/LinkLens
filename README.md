# 🔗 LinkLens

A minimal, clean webpage and YouTube transcript summarization tool powered by LangChain and Groq.

---

## ✨ Features

- 🌐 **Webpages & YouTube**: Summarize standard articles/webpages or load YouTube transcripts directly.
- 🧠 **Verbose Thinking**: View the AI's reasoning step-by-step in an expandable container.
- 🎨 **Minimal UI**: Clean, monochromatic layout that adapts natively to both dark and light modes.
- ⚡ **Streamlit Interface**: Lightweight, side-by-side control interface.

---

## 🏗️ Tech Stack

- Python
- Streamlit
- LangChain / LangChain Classic / LangChain Core
- Groq (ChatGroq API)
- Unstructured (Web document loader)
- YouTube Transcript API (Video transcript loader)

---

## 🚀 Getting Started

### Clone the repository

```bash
git clone https://github.com/itslokeshx/LinkLens.git
cd LinkLens
```

### Setup environment

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
streamlit run app.py
```

---

## 💡 How It Works

```text
               Input URL
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
  [ YouTube URL? ]    [ Standard URL? ]
         │                   │
         ▼                   ▼
   YoutubeLoader    UnstructuredLoader
         │                   │
         └─────────┬─────────┘
                   ▼
         Load Document Text
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
  Extract Thinking    Generate Summary
         │                   │
         ▼                   ▼
   st.expander          st.markdown
```

---

## 📂 Project Structure

```text
LinkLens/
├── app.py              # Application entry point and layout
├── requirements.txt    # Declared dependencies
├── .env.example        # Environment template file
└── README.md           # Documentation
```

---

## 📄 License

This project is licensed under the MIT License.
