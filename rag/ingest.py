from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb
import os

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(path="rag/chroma_db")

collection = client.get_or_create_collection(
    name="medical_docs"
)


def read_pdf(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text


def ingest_documents():

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    documents_folder = "documents"

    doc_id = 0

    for file in os.listdir(documents_folder):

        if file.endswith(".pdf"):

            pdf_path = os.path.join(
                documents_folder,
                file
            )

            text = read_pdf(pdf_path)

            chunks = splitter.split_text(text)

            for chunk in chunks:

                embedding = embedding_model.encode(
                    chunk
                ).tolist()

                collection.add(
                ids=[str(doc_id)],
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[{"source": file}]
                )

                doc_id += 1

    print("Documents Ingested Successfully")


if __name__ == "__main__":
    ingest_documents()