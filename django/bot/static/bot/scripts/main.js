"use strict";
import { handleBtnInputs, handleUserInput } from "./handlers.js";

const user_input = document.getElementById("user_msg");

const bot_btns = document.getElementById("bot-btns");
const bot_text_box = document.getElementById("bot-msg-text");
const send_message_btn = document.getElementById("send_message_btn");

// EVENT LISTENERS
send_message_btn.addEventListener("click", function (e) {
  handleUserInput(e, bot_text_box, bot_btns, user_input);
});
bot_btns.addEventListener("click", function (e) {
  handleBtnInputs(e);
});
