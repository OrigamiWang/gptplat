function tts(sentence) {
    let msg = new SpeechSynthesisUtterance(sentence);

    window.speechSynthesis.speak(msg);
}

function text_to_speach(div) {
    div.addEventListener("click", () => {
        tts(div.innerText)
    })
}


