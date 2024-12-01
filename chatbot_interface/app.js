document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("chat-form");
    const input = document.getElementById("user-input");
    const messagesDiv = document.getElementById("messages");

    function addMessage(text, sender = "bot") {
        const message = document.createElement("div");
        message.classList.add("message", sender);
        message.textContent = text;
        messagesDiv.appendChild(message);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
    form.addEventListener("submit", (event) => {
        event.preventDefault();
        const userMessage = input.value;
        addMessage(userMessage, "user");

        fetch("http://localhost:5005/webhooks/rest/webhook", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ sender: "user", message: "Hello" }),
        })
            .then((response) => response.json())
            .then((data) => {
                data.forEach((botMessage) => {
                    addMessage(botMessage.text, "bot");
                })
            })
            .catch((error) => {
                console.error("Error:", error);
                addMessage("Error connecting to chatbot.", "bot");
            });

        input.value = "";
    })
})
