<template>
  <div class="ChatWindow">
    <div
      v-for="message in messages"
      :key="message.text"
      :class="`ChatItem ${
        message.type === 'bot' ? 'ChatItem--customer' : 'ChatItem--expert'
      }`"
    >
      <div class="ChatItem-meta">
        <div class="ChatItem-avatar">
          <img
            class="ChatItem-avatarImage"
            v-if="message.type === 'bot'"
            src="https://image.ibb.co/eTiXWa/avatarrobot.png"
          />
          <img
            v-else
            width="48"
            height="48"
            src="https://img.icons8.com/color/96/circled-user-male-skin-type-6--v1.png"
            alt="circled-user-male-skin-type-6--v1"
          />
        </div>
      </div>
      <div class="ChatItem-chatContent">
        <div class="ChatItem-chatText">{{ message.text }}</div>
        <div class="ChatItem-timeStamp">
          <strong>{{ message.type }}</strong> • {{ message.timestamp }}
        </div>
      </div>
    </div>
    <!--    <button @click="startRecording">Record</button>-->
    <!--    <button @click="stopRecording">Stop</button>-->
    <!--    <input v-model="context" />-->

    <div class="ChatInput is-hidey">
      <input
        class="ChatInput-input"
        @keyup.enter="handleMessageInput"
        v-model="message"
      />

      <button @click="handleMessageInput">Send</button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import $ from "jquery";
import axios from "axios";

const message = ref("");

const handleMessageInput = async (e) => {
  if (context.value === "") {
    // add message to messages array
    messages.value.push({
      type: "human",
      text: `Selected context: ${message.value}`,
      timestamp:
        "Today  at" + new Date().getHours() + ":" + new Date().getMinutes(),
    });

    const response = await axios.post("http://127.0.0.1:8000/context", {
      context: message.value,
    });

    context.value = message.value;

    $(".ChatWindow").animate(
      { scrollTop: $(".ChatWindow").prop("scrollHeight") },
      500
    );

    messages.value.push({
      type: "bot",
      text: response.data,
      timestamp:
        "Today at " + new Date().getHours() + ":" + new Date().getMinutes(),
    });

    $(".ChatWindow").animate(
      { scrollTop: $(".ChatWindow").prop("scrollHeight") },
      500
    );
  } else {
    // add message to messages array
    messages.value.push({
      type: "human",
      text: message.value,
      timestamp:
        "Today  at" + new Date().getHours() + ":" + new Date().getMinutes(),
    });

    const response = await axios.post("http://127.0.0.1:8000/", {
      question: message.value,
      context: context.value,
    });

    message.value = "";

    $(".ChatWindow").animate(
      { scrollTop: $(".ChatWindow").prop("scrollHeight") },
      500
    );

    messages.value.push({
      type: "bot",
      text: response.data,
      timestamp:
        "Today at " + new Date().getHours() + ":" + new Date().getMinutes(),
    });

    $(".ChatWindow").animate(
      { scrollTop: $(".ChatWindow").prop("scrollHeight") },
      500
    );
  }
};

const messages = ref([
  {
    type: "bot",
    text: "Insert the context on which you want to ask a question",
    timestamp:
      "Today at " + new Date().getHours() + ":" + new Date().getMinutes(),
  },
]);
const context = ref("");
</script>

<style lang="sass">
$blue: #007FEF
$borderRadiusBase: 3px
$chatWidth: 48rem
$chatInputWidth: $chatWidth
$chatBackground: #eee
$chatInputHeight: 5rem
$chatInputInnerHeight: $chatInputHeight - 2rem

*
  box-sizing: border-box

body
  min-height: 100vh
  display: flex
  justify-content: center
  background: $blue
  font-family: 'Roboto', sans-serif

strong
  font-weight: bold

.ChatWindow
  width: $chatWidth
  height: 75vh
  padding: 2.5rem
  padding-bottom: $chatInputHeight + 1.5rem
  overflow: hidden
  overflow-y: auto
  align-self: flex-end
  background: $chatBackground
  box-shadow: 0 0 12px rgba(black, 0.3)
  border-radius: $borderRadiusBase $borderRadiusBase 0 0

.ChatItem
  display: flex
  justify-content: flex-start
  align-items: flex-start
  width: 100%
  margin-bottom: 2rem

.ChatItem--expert
  flex-direction: row-reverse

.ChatItem-meta
  display: flex
  align-items: center
  flex: 0 1 auto
  margin-right: 1rem
  margin-bottom: 0.5rem
  width: 2.5rem

  .ChatItem--expert &
    margin-right: 0
    margin-left: 1rem

.ChatItem-chatContent
  position: relative
  flex: 1 0 auto
  width: 100%

.ChatItem-avatar
  width: 2.5rem
  height: 2.5rem

  .ChatItem--expert &
    margin-right: 0

.ChatItem-avatarImage
  max-width: 100%
  border-radius: 100em

.ChatItem-avatarInitials
  display: flex
  align-items: center
  justify-content: center
  width: 2.5rem
  height: 2.5rem
  background: #ccc
  color: #444
  border-radius: 100em

.ChatItem-timeStamp
  width: 70%
  font-size: 0.875rem
  color: #666

  .ChatItem--expert &
    margin-left: auto

.ChatItem-chatText
  position: relative
  width: 70%
  margin-bottom: 0.5rem
  padding: 1rem
  background: $blue
  color: #fff
  border-radius: $borderRadiusBase
  box-shadow: 0 2px 6px rgba(#000, 0.175)
  line-height: 1.3

  &:first-child::before
    content: ''
    display: block
    position: absolute
    top: 0
    left: -0.4rem
    width: 1rem
    height: 1rem
    transform: scaleX(0.8) skew(45deg)
    background: $blue

    .ChatItem--expert &
      right: -0.4rem
      left: auto
      transform: skew(-40deg)
      background: #fff
      background: #fff
      box-shadow: 4px 0 4px -1px rgba(#000, 0.1)

  .ChatItem--expert &
    margin-left: auto
    border: 1px solid #dbdbdb
    background: white
    color: #666

.ChatItem-chatText > div
  display: inline

.ChatInput
  position: fixed
  bottom: 0
  left: 50%
  z-index: 10
  width: $chatInputWidth
  height: $chatInputHeight
  transform: translateX(-50%)
  background: $chatBackground

.ChatInput-input
  position: absolute
  right: 0
  bottom: 0
  left: 0
  width: 100%
  height: $chatInputHeight
  padding: 1rem 1.5rem
  padding-right: 5.25rem
  border: 0
  border-top: 1px solid #ccc
  overflow: hidden
  overflow-y: scroll
  background: #fff
  box-shadow: 0 0 4px rgba(#000, 0.1)
  font-size: 1rem
  resize: none


[contenteditable]:empty:before
  content: attr(placeholder)
  display: block
  color: #999

[contenteditable]:active,
[contenteditable]:focus
  border: 0
  border-top: 1px solid #ccc
  outline: 0
  box-shadow: inherit

.ChatInput-btnSend
  display: block
  position: absolute
  top: 50%
  right: 1.5rem
  transform: translateY(-50%)
  border: none
  border-radius: $borderRadiusBase
  background: $blue
  font-size: 1rem
  padding: 0.5rem 1rem
  color: white
  cursor: pointer
</style>
