let socketio = io()

let messages_div = document.getElementById("messages_div")
let old_messages = JSON.parse(document.getElementById("messages_input").value)
document.getElementById("message").addEventListener("keydown", handleKeyPress)
document.getElementById("odeslat_button").addEventListener("click", sendMessage)
let prodleva = document.getElementById("prodleva").value

let last_message_datetime = new Date()
let modal_is_active = false

let modal = document.getElementById("upozorneni_modal")
let modal_content = document.getElementById("modal_content")
window.onclick = function(event) {
    if (event.target == modal || event.target == modal_content) {
        modal.style.display = "none"
        modal_is_active = false
    }
}



old_messages.forEach(element => {
    createMessage(element.name, element.text, element.time, element.type)
});

socketio.on("message", (data) => {
    createMessage(data.name, data.text, data.time, data.type)
    if (data.type == "connection") {
    } else {
        let current_datetime = new Date()
        let delta = (current_datetime - last_message_datetime) / 1000
        if (delta > prodleva && !modal_is_active) {
            modal.style.display = "block"
            modal_is_active = true
            let popup_message = "Zpráva z " + data.time + " přišla o více než " + String(prodleva) + " sekund po předchozí zprávě, proto toto upozornění."
            document.getElementById("popup_message").innerText = popup_message
        } else {
            last_message_datetime = new Date()
        }
    }
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
    last_message_datetime = new Date()
}

function handleKeyPress(event) {
    if (event.key == "Enter") {
        sendMessage()
    } 
}