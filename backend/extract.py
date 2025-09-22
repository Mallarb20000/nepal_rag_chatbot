import PyPDF2
import os
import re

def extract_text_from_pdf(pdf_path):
    """Opens and reads a PDF file, returning its text content."""
    if not os.path.exists(pdf_path):
        print(f"Error: The file was not found at {pdf_path}")
        return None
    text = ""
    print(f"Reading PDF from: {pdf_path}")
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            print(f"Found {num_pages} pages to extract.")
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"An error occurred while reading the PDF: {e}")
        return None
    return text

def clean_and_chunk_text(text):
    """Cleans the text and splits it into logical chunks."""
    print("Cleaning and chunking text...")
    # Replace multiple newlines with a single one to normalize paragraph spacing
    text = re.sub(r'\n\s*\n', '\n\n', text)
    # Remove page numbers and the source citations like ''
    text = re.sub(r'\'', '', text)
    text = re.sub(r'^\d+\s*\n', '', text, flags=re.MULTILINE)

    # Split the text into potential chunks based on double newlines (paragraphs)
    chunks = text.split('\n\n')
    
    # Filter out any very small or empty chunks and strip whitespace
    meaningful_chunks = [chunk.strip() for chunk in chunks if len(chunk.strip()) > 100]
    
    print(f"Split the text into {len(meaningful_chunks)} meaningful chunks.")
    return meaningful_chunks

if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    project_root = os.path.dirname(script_dir)
    pdf_file_path = os.path.join(project_root, 'constitution.pdf')

    extracted_text = extract_text_from_pdf(pdf_file_path)
    
    if extracted_text:
        chunks = clean_and_chunk_text(extracted_text)


        # --- FINAL ADDITION ---
        # The first 4 chunks were the table of contents, so we skip them.
        final_chunks = chunks[4:] 
        print(f"Skipped the first 4 chunks. Using {len(final_chunks)} final chunks for the knowledge base.")
        
         # Let's save these clean chunks to a new file for inspection
        output_txt_path = os.path.join(project_root, 'constitution_cleaned.txt')
        with open(output_txt_path, 'w', encoding='utf-8') as f:
            for i, chunk in enumerate(final_chunks):
                f.write(f"--- CHUNK {i+1} ---\n")
                f.write(chunk.strip() + "\n\n")
        print(f"Saved the final cleaned chunks to {output_txt_path}")