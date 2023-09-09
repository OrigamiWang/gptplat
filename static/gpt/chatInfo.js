function enter_conversation_change_cursor(div, flag) {
    div.addEventListener("mouseenter", () => {
        body.style.cursor = "pointer"
        if (flag === 0) {
            div.setAttribute('class', 'conversation conversation_border')
        } else {
            div.setAttribute('class', 'conversation right conversation_border')
        }
    })
}

function leave_conversation_change_cursor(div, flag) {
    div.addEventListener("mouseleave", () => {
        body.style.cursor = ""
        if (flag === 0) {
            div.setAttribute('class', 'conversation')
        } else {
            div.setAttribute('class', 'conversation right')
        }
    })
}

function addConversationEvents(div, flag) {
    enter_conversation_change_cursor(div, flag)
    leave_conversation_change_cursor(div, flag)
    // flag: 0为answer，flag: 1为question
}