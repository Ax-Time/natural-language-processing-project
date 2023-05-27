<template>

</template>

<script lang="ts" setup>

import Recorder from "recorder-js";
import { ref } from "vue";
import axios from "axios";
import $ from "jquery";

const audioContext = new (window.AudioContext || window.webkitAudioContext)();

const recorder = new Recorder(audioContext, {
  // An array of 255 Numbers
  // You can use this to visualize the audio stream
});

let isRecording = false;
let blob = null;

navigator.mediaDevices
  .getUserMedia({ audio: true })
  .then((stream) => recorder.init(stream))
  .catch((err) => console.log("Uh oh... unable to get stream...", err));

const message = ref("");

const startRecording = () => {
  recorder.start().then(() => {
    console.log("im here");
  });
};

const stopRecording = () => {
  recorder.stop().then(({ blob, buffer }) => {
    // create wav file from blob and buffer
    const form = new FormData();
    form.append("audio_file", blob, "test.wav");
    // send data as a file to server
    axios.post("http://localhost:8000/audio", form).then((res) => {
      messages.value.push({
        type: "human",
        text: res.data.given,
        timestamp:
          "Today  at" + new Date().getHours() + ":" + new Date().getMinutes(),
      });

      $(".ChatWindow").animate(
        { scrollTop: $(".ChatWindow").prop("scrollHeight") },
        500
      );

      messages.value.push({
        type: "bot",
        text: res.data.output,
        timestamp:
          "Today at " + new Date().getHours() + ":" + new Date().getMinutes(),
      });

      $(".ChatWindow").animate(
        { scrollTop: $(".ChatWindow").prop("scrollHeight") },
        500
      );
    });
    // buffer is an AudioBuffer
  });
};
</script>

<style scoped>

</style>
