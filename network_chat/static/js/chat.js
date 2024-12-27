document.getElementById("joinForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const nickname = document.getElementById("nickname").value.trim();
    const pin = document.getElementById("pin").value.trim();

    // Basic client-side validation
    if (nickname.length < 3 || nickname.length > 15) {
        alert("Nickname must be between 3 and 15 characters.");
        return;
    }
    if (!/^[a-zA-Z0-9]+$/.test(nickname)) {
        alert("Nickname can only contain letters and numbers.");
        return;
    }

    const socket = new WebSocket(`ws://127.0.0.1:8000/ws/chat?pin=${pin}&nickname=${nickname}`);

    socket.onopen = function () {
        document.getElementById("joinForm").style.display = "none";
        document.getElementById("chat").style.display = "block";
    };

    socket.onmessage = function (event) {
        const data = event.data;

        if (data.startsWith("USERS:")) {
            // Update online users
            document.getElementById("online_users").innerText = data.replace("USERS:", "");
        } else {
            // Display chat message
            const messagesDiv = document.getElementById("messages");
            messagesDiv.innerHTML += `<p>${data}</p>`;
            messagesDiv.scrollTop = messagesDiv.scrollHeight; // Auto-scroll
        }
    };

    socket.onerror = function () {
        alert("Failed to connect. Check your PIN or try again.");
    };

    function sendMessage() {
        const messageInput = document.getElementById("message_input");
        const message = messageInput.value.trim();
        if (message !== "") {
            socket.send(message);
            messageInput.value = "";
        }
    }

    document.getElementById("message_input").addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });

    document.querySelector("button[onclick='sendMessage()']").addEventListener("click", sendMessage);
});
