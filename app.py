import os
import uuid
from flask import Flask, request, render_template, jsonify
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredHTMLLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ✅ Gemini 1.5 Flash
llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash-latest",
    temperature=0.2,
    google_api_key="AIzaSyA7YdIMRXPIlHfPSsn3vN3ZkiffBQhhEy0"  # Replace with your actual key
)

# ✅ HuggingFace BGE embeddings
embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-large-en-v1.5"
)

def load_file(file_path, ext):
    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path)
    elif ext in [".html", ".htm"]:
        loader = UnstructuredHTMLLoader(file_path)
    else:
        return []
    return loader.load()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if not uploaded_file:
        return "No file uploaded", 400

    # ❌ Remove old files
    for f in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER, f))

    # ✅ Save new file
    ext = os.path.splitext(uploaded_file.filename)[1].lower()
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
    uploaded_file.save(file_path)

    documents = load_file(file_path, ext)
    if not documents:
        return "Unsupported file type or failed to load", 400

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)

    # ✅ In-memory vector DB (not persisted)
    # ✅ Force new isolated in-memory Chroma collection
    vectordb = Chroma.from_documents(
    documents=docs,
    embedding=embedding_model,
    collection_name=str(uuid.uuid4())  # 💡 unique ID avoids reuse
)



    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectordb.as_retriever())

    # ✅ Replace previous chain
    app.qa_chain = qa_chain

    return jsonify({"message": "File uploaded and processed!"})

@app.route('/ask', methods=['POST'])
def ask_question():
    question = request.json.get("question", "")
    if not hasattr(app, "qa_chain"):
        return jsonify({"answer": "Please upload a file first."})
    result = app.qa_chain.run(question)
    return jsonify({"answer": result})

if __name__ == '__main__':
    app.run(debug=True)