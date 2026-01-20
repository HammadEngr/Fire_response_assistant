"use strict";
import { handleBtnInputs, handleUserInput } from "./handlers.js";

const user_input = document.getElementById("user_msg");
const send_message_btn = document.getElementById("send_message_btn");
const chat_container = document.getElementById("chat_container");

// EVENT LISTENERS
send_message_btn.addEventListener("click", function (e) {
  handleUserInput(e, user_input);
});
user_input.addEventListener("keydown", function (e) {
  if (e.key === "Enter") {
    e.preventDefault();
    handleUserInput(e, user_input);
  }
});
chat_container.addEventListener("click", function (e) {
  handleBtnInputs(e);
});
