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
    # Debug logging
    print(f"Content-Type: {request.content_type}")
    print(f"Request method: {request.method}")
    print(f"Request body: {request.body}")
    print(f"Request data: {getattr(request, 'data', 'No data attribute')}")

    # Handle both JSON and form data
    question = None
    if hasattr(request, 'data') and request.data:
        question = request.data.get('question')
        print(f"Got question from request.data: {question}")
    else:
        import json
        try:
            data = json.loads(request.body)
            question = data.get('question')
            print(f"Got question from JSON body: {question}")
        except (json.JSONDecodeError, AttributeError) as e:
            print(f"JSON decode error: {e}")
            question = request.POST.get('question')
            print(f"Got question from POST: {question}")

    if not question:
        error_msg = {
            "error": "No question was provided.",
            "debug": {
                "content_type": request.content_type,
                "has_data": hasattr(request, 'data'),
                "data": str(getattr(request, 'data', 'None')),
                "body": str(request.body),
                "post": dict(request.POST)
            }
        }
        print(f"Returning 400 error: {error_msg}")
        return Response(error_msg, status=400)

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
        ollama_client = ollama.Client(host='https://mallarb369-my-ollama-server.hf.space')
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
        import traceback
        error_details = traceback.format_exc()
        print(f"ERROR: {str(e)}")
        print(f"TRACEBACK: {error_details}")
        return Response({
            "error": f"An error occurred: {str(e)}",
            "traceback": error_details
        }, status=500)