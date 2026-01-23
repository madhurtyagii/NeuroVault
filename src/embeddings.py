"""
Embeddings and vector database management for NeuroVault
Uses ChromaDB for semantic search
"""

import chromadb
from sentence_transformers import SentenceTransformer
import os

# Initialize ChromaDB client
db_path = "data/chroma_db"
os.makedirs(db_path, exist_ok=True)

# Use local embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# ChromaDB client
client = chromadb.PersistentClient(path=db_path)

def get_or_create_collection(collection_name="neurovault_docs"):
    """Get or create ChromaDB collection"""
    try:
        collection = client.get_collection(name=collection_name)
    except:
        collection = client.create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    return collection

def chunk_text(text, chunk_size=500, overlap=100):
    """
    Split text into overlapping chunks for better semantic search
    chunk_size: characters per chunk
    overlap: characters to repeat between chunks
    """
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        
        if chunk.strip():  # Only add non-empty chunks
            chunks.append(chunk)
        
        start = end - overlap
    
    return chunks

def add_document_to_db(doc_id, filename, content):
    """
    Add document to ChromaDB with embeddings
    
    Args:
        doc_id: unique document ID
        filename: original filename
        content: full text content
    """
    collection = get_or_create_collection()
    
    # Chunk the document
    chunks = chunk_text(content)
    
    if not chunks:
        return False
    
    # Create unique IDs for each chunk
    chunk_ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
    
    # Add to ChromaDB (it auto-embeds)
    collection.add(
        ids=chunk_ids,
        documents=chunks,
        metadatas=[
            {
                "source_file": filename,
                "doc_id": doc_id,
                "chunk_index": i
            }
            for i in range(len(chunks))
        ]
    )
    
    return True

def search_documents(query, top_k=5):
    """
    Search for relevant documents/chunks
    
    Args:
        query: search query from user
        top_k: number of results to return
    
    Returns:
        list of (text, source_file, score) tuples
    """
    collection = get_or_create_collection()
    
    try:
        results = collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        if not results or not results['documents']:
            return []
        
        # Format results
        formatted_results = []
        for i, doc in enumerate(results['documents'][0]):
            score = results['distances'][0][i] if 'distances' in results else 0
            metadata = results['metadatas'][0][i] if 'metadatas' in results else {}
            
            formatted_results.append({
                'text': doc,
                'source': metadata.get('source_file', 'Unknown'),
                'similarity': 1 - score  # Convert distance to similarity
            })
        
        return formatted_results
    
    except Exception as e:
        print(f"Search error: {str(e)}")
        return []

def delete_document_from_db(doc_id):
    """Delete all chunks of a document from ChromaDB"""
    collection = get_or_create_collection()
    
    try:
        # Get all chunk IDs for this document
        results = collection.get(
            where={"doc_id": {"$eq": doc_id}}
        )
        
        if results and results['ids']:
            collection.delete(ids=results['ids'])
            return True
    except Exception as e:
        print(f"Delete error: {str(e)}")
        return False

def clear_all_embeddings():
    """Clear all embeddings (for testing/reset)"""
    try:
        client.delete_collection(name="neurovault_docs")
        return True
    except:
        return False

def get_collection_stats():
    """Get stats about current collection"""
    collection = get_or_create_collection()
    count = collection.count()
    return {"total_chunks": count}
