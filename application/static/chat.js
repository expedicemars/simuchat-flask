import http_get from "./http_get.js"
let socketio = io()

let chat_data = JSON.parse(http_get("/load_chat"))
let old_messages = chat_data.last_messages
let prodleva = chat_data.prodleva 
let simulation_start_time = chat_data.start_time

let messages_div = document.getElementById("messages_div")
let message_input = document.getElementById("message")
let time_span = document.getElementById("time")

document.getElementById("odeslat_button").addEventListener("click", sendMessage)
message_input.addEventListener("keydown", handleKeyPress)

let last_message_datetime = new Date()
let modal_is_active = false
let is_admin = false
if (document.getElementById("is_admin").value == "True") {
    is_admin = true
}

let modal = document.getElementById("upozorneni_modal")
let modal_content = document.getElementById("modal_content")
window.onclick = function(event) {
    if (event.target == modal || event.target == modal_content) {
        modal.style.display = "none"
        modal_is_active = false
    }
}


old_messages.forEach(element => {
    createMessage(element.author, element.content, element.pretty_time, element.category)
});

socketio.on("message", (data) => {
    createMessage(data.author, data.content, data.pretty_time, data.category)
    if (data.category == "connection") {
    } else {

        let current_datetime = new Date()
        let delta = (current_datetime - last_message_datetime) / 1000
        const isDeltaValid = delta > prodleva;
        const isModalInactive = !modal_is_active;
        const isOrgMessageForNonAdmin = (data.category == "org" && !is_admin);
        const isPosadkaMessageForAdmin = (data.category == "posadka" && is_admin);

        if (isDeltaValid && isModalInactive && (isOrgMessageForNonAdmin || isPosadkaMessageForAdmin)) {
            modal.style.display = "block"
            modal_is_active = true
            let popup_message = "Zpráva v čase " + data.datetime + " přišla o více než " + String(prodleva) + " sekund po předchozí zprávě, proto toto upozornění."
            document.getElementById("popup_message").innerText = popup_message
            last_message_datetime = new Date()
        } else {
            last_message_datetime = new Date()
        }
    }
})

function createMessage(author, content, time, category) {
    let message_div = document.createElement("div")
    message_div.classList.add("message", `message-${category}`)

    let author_span = document.createElement("span")
    author_span.classList.add("author")
    author_span.innerText = author

    let content_span = document.createElement("span")
    content_span.classList.add("content")
    content_span.innerText = content

    let datetime_span = document.createElement("span")
    datetime_span.classList.add("datetime")
    datetime_span.innerText = time

    message_div.appendChild(author_span)
    message_div.appendChild(content_span)
    message_div.appendChild(datetime_span)

    messages_div.appendChild(message_div)

    messages_div.scrollTop = messages_div.scrollHeight
}

function sendMessage() {
    if (message_input.value == "") return
    socketio.emit("message", {content: message_input.value})
    message_input.value = ""
    last_message_datetime = new Date()
    modal.style.display = "none"
    modal_is_active = false
}


function handleKeyPress(event) {
    if (event.key == "Enter") {
        if (event.shiftKey) {
        } else {
            sendMessage()
            event.preventDefault()
        }
    }
}

// parse the iso-formatted start time, compute the elapsed time, and update the time span every second
// the format is hh : mm : ss, when it overflows 24 hours, it continues counting in hours, e.g., 25 : 00 : 00
let start_datetime = new Date(simulation_start_time)
setInterval(() => {
    let current_datetime = new Date()
    let elapsed_ms = current_datetime - start_datetime
    let elapsed_sec = Math.floor(elapsed_ms / 1000)
    let hours = Math.floor(elapsed_sec / 3600)
    let minutes = Math.floor((elapsed_sec % 3600) / 60)
    let seconds = elapsed_sec % 60
    let time_string = String(hours).padStart(2, '0') + " : " + String(minutes).padStart(2, '0') + " : " + String(seconds).padStart(2, '0')
    time_span.innerText = time_string
}, 1000)