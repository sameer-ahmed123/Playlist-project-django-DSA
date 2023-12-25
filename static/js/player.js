var myAudio = document.getElementById("audio_file");
var isPlaying = false;

let play_btn = document.getElementById("play_btn")

function togglePlay() {
    isPlaying ? myAudio.pause() : myAudio.play();
};

myAudio.onplaying = function () {
    isPlaying = true;
    play_btn.classList.remove("fa-play")
    play_btn.classList.add("fa-pause")
};
myAudio.onpause = function () {
    isPlaying = false;
    play_btn.classList.remove("fa-pause")
    play_btn.classList.add("fa-play")
};
