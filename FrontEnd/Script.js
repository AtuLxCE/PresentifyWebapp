function displayFileName() {
        const input = document.getElementById('pdf-upload');
        const fileNameInfo = document.getElementById('file-name-info');
        const uploadLabel = document.getElementById('upload-label');
        const fileName = input.files[0].name;
        fileNameInfo.textContent = `Selected file: ${fileName}`;
        fileNameInfo.classList.remove('hidden');
        uploadLabel.classList.add('hidden');
    }
    function postData() {
        const formData = new FormData(document.getElementById("myForm"));
        fetch('http://localhost:8000/extract-text', { // Assuming your FastAPI server is running locally on port 8000
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            // Do something with the response data
        })
        .catch(error => {
            console.error('Error:', error);
            // Handle error
        });
    }