"use strict";
import {
  handleBtnInputs,
  handleUserInput,
  handleQuickSection,
  handleSendLocation,
} from "./handlers.js";

const user_input = document.getElementById("user_msg");
const send_message_btn = document.getElementById("send_message_btn");
const chat_container = document.getElementById("chat_container");
const quick_section = document.querySelector(".quick-section");

// EVENT LISTENERS
let userLocation = null;
document.addEventListener("DOMContentLoaded", async function () {
  handleSendLocation();
});

send_message_btn.addEventListener("click", function (e) {
  handleUserInput(e, user_input, userLocation);
});
user_input.addEventListener("keydown", function (e) {
  if (e.key === "Enter") {
    e.preventDefault();
    handleUserInput(e, user_input, userLocation);
  }
});

quick_section.addEventListener("click", function (e) {
  handleQuickSection(e);
});

chat_container.addEventListener("click", function (e) {
  handleBtnInputs(e);
});
