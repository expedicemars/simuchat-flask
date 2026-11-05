import http_get from "./http_get.js"
let socketio = io()

let chat_data = JSON.parse(http_get("/load_chat"))
let old_messages = chat_data.last_messages
let prodleva = chat_data.prodleva 
let simulation_start_time = chat_data.start_time
let has_older_messages = chat_data.has_older_messages
let oldest_message_id = old_messages.length > 0 ? old_messages[0].id : null

let messages_div = document.getElementById("messages_div")
let message_input = document.getElementById("message")
let time_span = document.getElementById("time")
let older_messages_button = document.getElementById("older_messages_button")
let author_filter_button = document.getElementById("author_filter_button")
let author_filter_panel = document.getElementById("author_filter_panel")
let visible_authors = new Set()

document.getElementById("odeslat_button").addEventListener("click", sendMessage)
message_input.addEventListener("keydown", handleKeyPress)
older_messages_button.addEventListener("click", loadOlderMessages)
older_messages_button.disabled = !has_older_messages
if (author_filter_button && author_filter_panel) {
    author_filter_button.addEventListener("click", toggleAuthorFilter)
}

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
    createMessage(element.id, element.author, element.content, element.pretty_time, element.category, element.status)
});

function toggleAuthorFilter() {
    let is_open = !author_filter_panel.hidden
    author_filter_panel.hidden = is_open
    author_filter_button.setAttribute("aria-expanded", String(!is_open))
}

function addAuthorToFilter(author) {
    if (!author_filter_panel || visible_authors.has(author)) return
    visible_authors.add(author)

    let label = document.createElement("label")
    label.classList.add("author-filter-option")

    let checkbox = document.createElement("input")
    checkbox.type = "checkbox"
    checkbox.checked = true
    checkbox.value = author
    checkbox.addEventListener("change", applyAuthorFilter)

    label.appendChild(checkbox)
    label.appendChild(document.createTextNode(` ${author}`))
    author_filter_panel.appendChild(label)
}

function applyAuthorFilter() {
    let selected_authors = new Set(
        Array.from(author_filter_panel.querySelectorAll("input:checked"))
            .map(checkbox => checkbox.value)
    )
    messages_div.querySelectorAll(".message").forEach(message => {
        message.hidden = !selected_authors.has(message.dataset.author)
    })
}

function loadOlderMessages() {
    if (!has_older_messages || oldest_message_id === null) return

    let response = JSON.parse(http_get("/load_older_messages?before_id=" + oldest_message_id))
    let previous_scroll_height = messages_div.scrollHeight
    response.messages.forEach(element => {
        createMessage(element.id, element.author, element.content, element.pretty_time, element.category, element.status, true)
    })
    if (response.messages.length > 0) {
        oldest_message_id = response.messages[0].id
        messages_div.scrollTop += messages_div.scrollHeight - previous_scroll_height
    }
    has_older_messages = response.has_older_messages
    older_messages_button.disabled = !has_older_messages
}

socketio.on("message", (data) => {
    createMessage(data.id, data.author, data.content, data.pretty_time, data.category, data.status)
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

socketio.on("message_status", (data) => {
    updateMessageStatus(data.message_id, data.status)
})

function createMessage(id, author, content, time, category, status = "none", prepend = false) {
    addAuthorToFilter(author)

    let message_div = document.createElement("div")
    message_div.classList.add("message", `message-${category}`)
    message_div.dataset.messageId = id
    message_div.dataset.author = author
    message_div.dataset.status = status
    message_div.addEventListener("click", () => {
        let next_status = {
            none: "acknowledged",
            acknowledged: "alert",
            alert: "none"
        }[message_div.dataset.status]
        socketio.emit("message_status", {
            message_id: id,
            status: next_status
        })
    })

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
    let status_span = document.createElement("span")
    status_span.classList.add("message-status")
    message_div.appendChild(status_span)

    if (prepend && messages_div.firstChild) {
        messages_div.insertBefore(message_div, messages_div.firstChild)
    } else {
        messages_div.appendChild(message_div)
    }
    updateMessageStatus(id, status)

    if (!prepend) {
        messages_div.scrollTop = messages_div.scrollHeight
    }
}

function updateMessageStatus(id, status) {
    let message_div = Array.from(messages_div.querySelectorAll(".message"))
        .find(message => String(message.dataset.messageId) === String(id))
    if (!message_div) return

    message_div.dataset.status = status
    message_div.querySelector(".message-status").innerText = {
        none: "",
        acknowledged: "✅",
        alert: "🚨"
    }[status] || ""
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