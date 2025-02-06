import os
import PyPDF2
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import google.generativeai as genai
from werkzeug.utils import secure_filename

# Configure Google Generative AI
genai.configure(api_key="AIzaSyC-sBXY8Jsg758ypFm-BgVKsumypNjpLu4")
model = genai.GenerativeModel("gemini-2.0-flash-001", generation_config={"temperature": 0.7})

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Store last 10 queries and responses
history = []

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

# Function to chunk text
def chunk_text(text, chunk_size=500):
    words = text.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

# Function to embed text chunks
def embed_text_chunks(chunks):
    return embedder.encode(chunks)

# Function to store embeddings using FAISS
def store_embeddings(embeddings):
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index

# Function to retrieve relevant chunks
def retrieve_relevant_chunks(query, index, embeddings, chunks, k=5):
    query_embedding = embedder.encode([query])
    distances, indices = index.search(query_embedding, k)
    return [chunks[i] for i in indices[0]]

# Function to generate response with history
def generate_response(query, relevant_chunks):
    global history
    context = ' '.join(relevant_chunks)

    # Keep only the last 10 messages in history
    if len(history) > 10:
        history = history[-10:]

    # Build history context
    history_text = "\n".join([f"User: {q}\nBot: {r}" for q, r in history])
    prompt = f"Based on the following conversation history and context, answer the question:\n\nHistory:\n{history_text}\n\nContext: {context}\n\nUser: {query}\nBot:"

    response = model.generate_content(prompt)
    response_text = response.text

    # Add the new query-response pair to history
    history.append((query, response_text))

    return response_text

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    return jsonify({"message": "File uploaded successfully", "file_path": file_path})

@app.route('/query', methods=['POST'])
def query_pdf():
    data = request.get_json()
    pdf_path = data.get("file_path")
    query = data.get("query")
    
    if not pdf_path or not query:
        return jsonify({"error": "Missing file path or query"}), 400
    
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)
    embeddings = embed_text_chunks(chunks)
    index = store_embeddings(embeddings)
    relevant_chunks = retrieve_relevant_chunks(query, index, embeddings, chunks)
    response = generate_response(query, relevant_chunks)
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
