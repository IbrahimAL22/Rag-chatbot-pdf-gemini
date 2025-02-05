import PyPDF2
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import google.generativeai as genai

# Set up the API key from an environment variable
api_key = "AIzaSyC-sBXY8Jsg758ypFm-BgVKsumypNjpLu4"
if not api_key:
    raise ValueError("API key not found. Please set the GOOGLE_GENERATIVEAI_API_KEY environment variable.")

genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel("gemini-pro", generation_config={"temperature": 0.1})

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to chunk text
def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

# Function to embed text chunks
def embed_text_chunks(chunks):
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = embedder.encode(chunks)
    return embeddings

# Function to store embeddings using FAISS
def store_embeddings(embeddings):
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index

# Function to retrieve relevant chunks
def retrieve_relevant_chunks(query, index, embeddings, chunks, k=5):
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = embedder.encode([query])
    distances, indices = index.search(query_embedding, k)
    relevant_chunks = [chunks[i] for i in indices[0]]
    return relevant_chunks

# Function to generate response
def generate_response(query, relevant_chunks):
    context = ' '.join(relevant_chunks)
    prompt = f"Based solely on the following context , answer the question:\n\nContext: {context}\n\nQuestion: {query}\n\nAnswer:"
    response = model.generate_content(prompt)
    return response.text

# Main function to handle RAG
def rag_from_pdf(pdf_path, query):
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)
    embeddings = embed_text_chunks(chunks)
    index = store_embeddings(embeddings)
    relevant_chunks = retrieve_relevant_chunks(query, index, embeddings, chunks)
    response = generate_response(query, relevant_chunks)
    return response

# Example usage
pdf_path = '1-mvr-part-4-jan25.pdf'
query = 'give me precise resume of this document and mention all priciple subsections'
response = rag_from_pdf(pdf_path, query)
print(f"Response: {response}")
