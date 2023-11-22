let socketio = io()

let messages_div = document.getElementById("messages_div")
let old_messages = JSON.parse(document.getElementById("messages_input").value)
document.getElementById("message").addEventListener("keydown", handleKeyPress)
document.getElementById("odeslat_button").addEventListener("click", sendMessage)


old_messages.forEach(element => {
    createMessage(element.name, element.text, element.time, element.type)
});

socketio.on("message", (data) => {
    createMessage(data.name, data.text, data.time, data.type)
})

socketio.on("archivovani", (data) => {
    while (messages_div.firstChild && data["pocet"] < messages_div.children.length) {
        messages_div.removeChild(messages_div.firstChild);
    }
})

function createMessage(name, text, time, type) {
    let new_message = `
    <div class="message message-${type}">
        <span class="name">
            ${name}
        </span>
        <span class="text">
            ${text}
        </span>
        <span class="date">
            ${time}
        </span>
    </div>
    `
    messages_div.innerHTML += new_message
    messages_div.scrollTop = messages_div.scrollHeight
}

function sendMessage() {
    let message_input = document.getElementById("message")
    if (message_input.value == "") return
    socketio.emit("message", {text: message_input.value})
    message_input.value = ""
}

function handleKeyPress(event) {
    if (event.key == "Enter") {
        sendMessage()
    } 
}