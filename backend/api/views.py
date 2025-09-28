from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import chromadb
import ollama
import os

# We can remove the hello_world view now as it was just for testing
# def hello_world(request): ...

@csrf_exempt
@api_view(['POST'])
def chat(request):
    question = request.data.get('question')

    if not question:
        return Response({"error": "No question was provided."}, status=400)

    try:
        # --- RETRIEVAL PHASE ---
        db_client = chromadb.PersistentClient(path="/app/chroma_db")
        collection = db_client.get_collection(name="nepal_constitution")

        results = collection.query(query_texts=[question], n_results=3)
        context = "\n\n---\n\n".join(results['documents'][0])

        # --- GENERATION PHASE ---
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

        # Correctly connect to the Ollama client inside Docker
        ollama_client = ollama.Client(host='http://host.docker.internal:11434')
        response = ollama_client.chat(
            model='llama3:8b',
            messages=[{'role': 'user', 'content': prompt_template}]
        )
        final_answer = response['message']['content']
        
        return Response({
            "question": question,
            "answer": final_answer,
        })

    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)