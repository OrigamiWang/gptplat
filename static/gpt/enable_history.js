let enabled = true

function enable_history() {
    chatText.addEventListener("input", () => {
        if (enabled) {
            if (chatText.value === "Origami") {
                load_history()
                enabled = false
            }
        }
    })
}


