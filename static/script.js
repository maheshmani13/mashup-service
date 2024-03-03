// script.js

document.addEventListener('DOMContentLoaded', function() {
    // Get the form element
    const form = document.getElementById('form1');

    // Add a submit event listener to the form
    form.addEventListener('submit', function(event) {
        // Prevent the default form submission
        event.preventDefault();

        // Collect form data
        const formData = new FormData(form);
        const jsonData = {};
        formData.forEach((value, key) => {
            jsonData[key] = value;
        });
    

        alert("You will receive mashup file through mail in some time.Thank You!");

        // Make a Fetch API POST request
        fetch('/submitform', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(jsonData),
        })
    });
});
