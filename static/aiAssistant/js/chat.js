/**
 * Get cookie by name
 * @param name
 * @returns {null}
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}// getCookie
document.getElementById('chat-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value;
    messageInput.value = '';
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML += '<p><strong>You:</strong> ' + message + '</p>';
    fetch('/chat/', {
        method: 'POST', body: JSON.stringify({message: message}), headers: {
            'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => response.json())
        .then(data => {
            chatBox.innerHTML += '<p><strong>AI:</strong> ' + data.message + '</p>';
            chatBox.scrollTop = chatBox.scrollHeight;
        })
});

