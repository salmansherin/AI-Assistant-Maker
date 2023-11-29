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
    const threadId = document.getElementById('thread-id').value;
    const assistantId = document.getElementById('assistant-id').value;
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value;
    messageInput.value = '';
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML += '<p><strong style="color: green">USER:</strong> ' + message + '</p>';
    fetch('/chat', {
        method: 'POST', body: JSON.stringify({message: message}), headers: {
            'THREAD-ID': threadId,
            'ASSISTANT-ID': assistantId,
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        }
    })
        .then(response => response.json())
        .then(data => {
            chatBox.innerHTML = "";
            console.log(data)
            data.reverse().map(message => {
                let color = message.role === 'assistant' ? 'darkred' : 'green';
                chatBox.innerHTML += '<p><strong style="color: ' + color + '">' + message.role.toString().toUpperCase() + ':</strong> ' + message.content + '</p>';
            })
            chatBox.scrollTop = chatBox.scrollHeight;
        })
});

