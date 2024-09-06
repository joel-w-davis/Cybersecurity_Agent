import streamlit as st
import requests

# Set the URL of the Flask API
API_URL = "https://cybersecurity-agent-fu2eiqbyw-joel-davis-projects-7ca38eef.vercel.app/"

# Title of the Streamlit app
st.title("Cybersecurity Agent Q&A")

# Input prompt from the user
query = st.text_input("Enter your prompt:")

# Button to submit the query
if st.button("Submit"):
    if query:
        try:
            # Send POST request to Flask API
            response = requests.post(API_URL, json={"query": query})

            # If the response is successful, show the answer
            if response.status_code == 200:
                answer = response.json().get("answer", "No answer found")
                st.success(f"Answer: {answer}")
            else:
                error_message = response.json().get("error", "An error occurred")
                st.error(f"Error: {error_message}")

        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
    else:
        st.warning("Please enter a prompt.")
