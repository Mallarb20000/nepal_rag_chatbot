import chromadb
import os

def read_cleaned_chunks(file_path):
    """Reads the cleaned constitution text and splits it back into a list of chunks."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        print("Please make sure you have run the extract.py script first.")
        return []

    # Chunks are separated by '--- CHUNK [number] ---'
    # We can split by '--- CHUNK' and then clean up
    raw_chunks = content.split('--- CHUNK')[1:] # The first split is empty
    
    cleaned_chunks = []
    for raw_chunk in raw_chunks:
        # Split at the first newline to separate the header (e.g., ' 1 ---\n') from the text
        parts = raw_chunk.split('\n', 1)
        if len(parts) == 2:
            cleaned_chunks.append(parts[1].strip())
            
    return cleaned_chunks

def main():
    script_dir = os.path.dirname(__file__)
    project_root = os.path.dirname(script_dir)
    cleaned_file_path = os.path.join(project_root, 'constitution_cleaned.txt')

    print("Reading cleaned text chunks...")
    documents = read_cleaned_chunks(cleaned_file_path)
    
    if not documents:
        print("No documents found to populate the database.")
        return

    print(f"Found {len(documents)} documents to load.")

    # This creates a persistent database in a folder named 'chroma_db' in your project root
    client = chromadb.PersistentClient(path=os.path.join(project_root, "chroma_db"))
    
    # Get or create a "collection" (like a table in a SQL database)
    # The default embedding model is very capable and will be downloaded automatically
    collection = client.get_or_create_collection(name="nepal_constitution")

    print("Embedding documents and adding them to the ChromaDB collection. This might take a moment...")
    
    # Add the documents to the collection. ChromaDB handles the embedding for us.
    # We also need to provide a unique ID for each chunk.
    collection.add(
        documents=documents,
        ids=[f"chunk_{i}" for i in range(len(documents))]
    )

    print("✅ Successfully populated the ChromaDB collection.")
    print(f"The collection now contains {collection.count()} items.")

if __name__ == "__main__":
    main()