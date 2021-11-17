const startBtn = document.querySelector("#start-btn");

const recognition = new webkitSpeechRecognition();
recognition.continuous = true;
recognition.lang = "en-US";
recognition.interimResults = false;
recognition.maxAlternative = 1;

const synth = window.speechSynthesis;

startBtn.addEventListener("click", () => {
    recognition.start();
});

recognition.onresult = (e) => {
    console.log()
    const transcript = e.results[e.results.length - 1][0].transcript.trim();
    if(transcript == "hello"){
        const utter = new SpeechSynthesisUtterance("my name is hari");
        synth.speak(utter);
    }
};