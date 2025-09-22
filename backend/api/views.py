from rest_framework.decorators import api_view
from rest_framework.response import Response
import chromadb
import ollama
import os

@api_view(['POST'])
def chat(request):
    # 1. Get the user's question from the request
    question = request.data.get('question')

    if not question:
        return Response({"error": "No question was provided."}, status=400)

    try:
        # --- RETRIEVAL PHASE ---
        # 2. Connect to ChromaDB and get the collection
        script_dir = os.path.dirname(__file__)
        project_root = os.path.dirname(script_dir)
        # The DB is in the root, so we go up one level from `backend`
        client = chromadb.PersistentClient(path=os.path.join(project_root, "../chroma_db")) 
        collection = client.get_collection(name="nepal_constitution")

        # 3. Query the database to find the 3 most relevant chunks
        results = collection.query(
            query_texts=[question],
            n_results=3 
        )
        retrieved_chunks = results['documents'][0]
        context = "\n\n---\n\n".join(retrieved_chunks)

        # --- GENERATION PHASE ---
        # 4. Construct a detailed prompt for the LLM
        prompt_template = f"""
        You are an expert assistant on the Constitution of Nepal.
        Answer the following question based ONLY on the context provided below.
        If the answer is not in the context, say "I cannot answer this question based on the provided context."

        CONTEXT:
        {context}

        QUESTION:
        {question}

        ANSWER:
        """

        # 5. Send the prompt to the Ollama model
        response = ollama.chat(
            model='llama3:8b', 
            messages=[{'role': 'user', 'content': prompt_template}]
        )
        final_answer = response['message']['content']
        
        # 6. Return the final answer
        return Response({
            "question": question,
            "answer": final_answer,
        })

    except Exception as e:
        # Handle potential errors, e.g., if ChromaDB or Ollama is not running
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)