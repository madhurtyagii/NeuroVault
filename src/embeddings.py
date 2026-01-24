import chromadb
from chromadb.config import Settings
import os

# Initialize ChromaDB client
CHROMA_PATH = "data/chroma_db"
os.makedirs(CHROMA_PATH, exist_ok=True)

client = chromadb.PersistentClient(
    path=CHROMA_PATH,
    settings=Settings(
        anonymized_telemetry=False,
        allow_reset=True
    )
)

COLLECTION_NAME = "neurovault_documents"

def get_collection():
    """Get or create the ChromaDB collection"""
    try:
        collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        return collection
    except Exception as e:
        print(f"Error getting collection: {e}")
        raise

def chunk_text(text, chunk_size=500, overlap=50):
    """
    Split text into overlapping chunks
    
    Args:
        text: Input text
        chunk_size: Target size of each chunk (in characters)
        overlap: Overlap between chunks
    
    Returns:
        List of text chunks
    """
    if not text or not text.strip():
        return []
    
    words = text.split()
    chunks = []
    
    # Calculate words per chunk (approximate)
    words_per_chunk = chunk_size // 5  # Avg 5 chars per word
    overlap_words = overlap // 5
    
    for i in range(0, len(words), words_per_chunk - overlap_words):
        chunk = ' '.join(words[i:i + words_per_chunk])
        if chunk.strip():
            chunks.append(chunk)
    
    return chunks

def add_document_to_db(doc_id, filename, content):
    """
    Add document to ChromaDB with chunking
    
    Args:
        doc_id: Unique document identifier
        filename: Name of the file
        content: Text content to embed
    
    Returns:
        bool: Success status
    """
    try:
        collection = get_collection()
        
        # Split content into chunks
        chunks = chunk_text(content)
        
        if not chunks:
            print("Warning: No chunks created from content")
            return False
        
        # Generate IDs and metadata for each chunk
        ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"filename": filename, "chunk_index": i} for i in range(len(chunks))]
        
        # Add to collection
        collection.add(
            documents=chunks,
            ids=ids,
            metadatas=metadatas
        )
        
        print(f"✅ Added {len(chunks)} chunks for {filename}")
        return True
    
    except Exception as e:
        print(f"Error adding document: {e}")
        import traceback
        traceback.print_exc()
        return False

def delete_document_from_db(doc_id):
    """
    Delete all chunks of a document from ChromaDB
    
    Args:
        doc_id: Document identifier to delete
    
    Returns:
        bool: Success status
    """
    try:
        collection = get_collection()
        
        # Get all IDs for this document
        all_items = collection.get()
        doc_ids = [id for id in all_items['ids'] if id.startswith(f"{doc_id}_chunk_")]
        
        if doc_ids:
            collection.delete(ids=doc_ids)
            print(f"✅ Deleted {len(doc_ids)} chunks for {doc_id}")
        else:
            print(f"⚠️ No chunks found for {doc_id}")
        
        return True
    
    except Exception as e:
        print(f"Error deleting document: {e}")
        import traceback
        traceback.print_exc()
        return False

def search_documents(query, top_k=5):
    """
    Search for relevant documents using semantic similarity
    
    Args:
        query: Search query text
        top_k: Number of results to return
    
    Returns:
        List of dicts with keys: text, filename, distance
    """
    try:
        collection = get_collection()
        
        # Check if collection has documents
        if collection.count() == 0:
            print("Warning: Collection is empty")
            return []
        
        # Perform search
        results = collection.query(
            query_texts=[query],
            n_results=top_k,
            include=['documents', 'distances', 'metadatas']
        )
        
        # Format results
        formatted_results = []
        if results['documents'] and len(results['documents'][0]) > 0:
            for i in range(len(results['documents'][0])):
                # Get metadata for filename
                metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                filename = metadata.get('filename', 'Unknown')
                
                formatted_results.append({
                    'text': results['documents'][0][i],
                    'filename': filename,
                    'distance': results['distances'][0][i]
                })
        
        return formatted_results
    
    except Exception as e:
        print(f"Search error: {e}")
        import traceback
        traceback.print_exc()
        return []

def get_collection_stats():
    """Get statistics about the collection"""
    try:
        collection = get_collection()
        count = collection.count()
        return {
            "total_chunks": count,
            "collection_name": COLLECTION_NAME
        }
    except Exception as e:
        print(f"Error getting stats: {e}")
        return {"total_chunks": 0, "collection_name": COLLECTION_NAME}
