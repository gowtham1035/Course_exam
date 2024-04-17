// Function to fetch threads from the server
function fetchThreads() {
    fetch('/threads')
    .then(response => response.json())
    .then(data => {
        const threadsList = document.getElementById('threads-list');
        threadsList.innerHTML = '';
        data.forEach(thread => {
            const threadItem = document.createElement('li');
            threadItem.textContent = `${thread.title} - ${thread.user}`;
            threadsList.appendChild(threadItem);
        });
    })
    .catch(error => console.error('Error fetching threads:', error));
}

// Fetch threads on page load
fetchThreads();

// Event listener for creating a new thread
document.getElementById('create-thread-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch('/create_thread', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            fetchThreads();
            this.reset();
        } else {
            console.error('Failed to create thread');
        }
    })
    .catch(error => console.error('Error creating thread:', error));
});
