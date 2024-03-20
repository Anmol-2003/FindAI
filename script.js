document.getElementById('sendButton').addEventListener('click', function () {
    const textInput = document.getElementById('textInput').value;
    console.log(textInput);

    fetch("http://192.168.1.34:3000/detect", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: textInput }),
    })
        .then(response => response.json())
        .then(data => {

            document.getElementById('textInput').blur();

            const responseDiv = document.getElementById('response');
            responseDiv.textContent = data.percentage.toString() + '%';
            
            // Show the response and blur the text input box
            responseDiv.classList.remove('response-hidden');

        })
        .catch((error => {
            console.error("Error: ", error);
        }))
})