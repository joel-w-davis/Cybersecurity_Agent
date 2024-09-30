
    const API_URL = "http://127.0.0.1:5000"; // Flask API endpoint

    function submitQuery() {
        const query = document.getElementById('queryInput').value;
        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = '';  // Clear previous result

        if (!query) {
            resultDiv.innerHTML = '<p class="error">Please enter a prompt.</p>';
            return;
        }

        // Send POST request to Flask API
        fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        })
        .then(response => response.json())
        .then(data => {
            if (data.answer) {
                resultDiv.innerHTML = `<p class="success">Answer: ${data.answer}</p>`;
            } else if (data.error) {
                resultDiv.innerHTML = `<p class="error">Error: ${data.error}</p>`;
            } else {
                resultDiv.innerHTML = `<p class="error">An unknown error occurred.</p>`;
            }
        })
        .catch(error => {
            resultDiv.innerHTML = `<p class="error">An unexpected error occurred: ${error.message}</p>`;
        });
}

