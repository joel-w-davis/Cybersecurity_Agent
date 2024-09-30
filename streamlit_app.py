from flask import Flask, request, jsonify
import os
import time
from uuid import uuid4
import openai
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from dotenv import find_dotenv, load_dotenv



# Load environment variables
load_dotenv(find_dotenv())

# Initialize the app
app = Flask(__name__)

# Environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')

# Pinecone Initialization
pc = Pinecone(api_key=PINECONE_API_KEY)

# Index setup
index_name = "cyber-bot"
spec = ServerlessSpec(cloud='aws', region='us-east-1')

# Create index if not exists
existing_indexes = [index_info['name'] for index_info in pc.list_indexes()]
if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=spec,
    )
    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)

# Get index instance
index = pc.Index(index_name)

# Initialize vector store and OpenAI embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=OPENAI_API_KEY)
vector_store = PineconeVectorStore(index=index, embedding=embeddings)

# LLM setup
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-4", temperature=0.2)
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vector_store.as_retriever())

# Route for question answering
@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        # Get user query from request
        data = request.get_json()
        query = data.get('query')

        if not query:
            return jsonify({"error": "Query is required"}), 400

        # Perform the retrieval and question answering
        answer = qa.run(query)

        return jsonify({"answer": answer}), 200

    except openai.error.OpenAIError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Start the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

