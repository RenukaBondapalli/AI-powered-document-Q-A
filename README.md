# 🤖 AI-Powered Document Q&A

Upload any document and ask natural language questions to extract instant answers. This Retrieval-Augmented Generation (RAG) system uses:

- 🧠 Google Gemini 1.5 Flash as the LLM  
- 🌐 HuggingFace BGE Large embeddings  
- 🔍 LangChain for retrieval-based Q&A  
- ⚡ In-memory Chroma vector store  
- 🧾 Supports `.pdf`, `.txt`, `.html` documents  
- 🧠 Built with Python + Flask

---

### 🎥 Live Demo Video

[👉 Click here to watch the demo](https://drive.google.com/file/d/1wkoR6cOAd2hJ1iNxeSCa_GyWoLhndMZl/view?usp=drivesdk)

---

## 🚀 Features

- Upload documents and process them in-memory
- Ask contextual questions based on document content
- Supports PDF, TXT, and HTML
- Stateless: no DB, no storage, no reuse of past sessions
- Uses Gemini 1.5 Flash + BGE embeddings for fast and accurate results

---

## 🛠️ Tech Stack

| Layer        | Tool/Model                       |
|--------------|----------------------------------|
| LLM          | Google Gemini 1.5 Flash          |
| Embeddings   | BAAI/bge-large-en-v1.5           |
| Vector Store | Chroma (in-memory)               |
| Backend      | Flask                            |
| Document Parsing | LangChain Community Loaders  |
| Frontend     | Simple HTML + JavaScript         |
